import os
import smtplib
# comment out below line to enable tensorflow outputs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
from absl import app, flags, logging
from absl.flags import FLAGS
import core.utils as utils
from core.yolov4 import filter_boxes
from core.functions import *
from tensorflow.python.saved_model import tag_constants
from PIL import Image
import cv2
import numpy as np
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
from twilio.rest import Client

# Flag Sections

flags.DEFINE_string('framework', 'tf', '(tf, tflite, trt')
flags.DEFINE_string('weights', './checkpoints/yolov4-416',
                    'path to weights file')
flags.DEFINE_integer('size', 416, 'resize images to')
flags.DEFINE_boolean('tiny', False, 'yolo or yolo-tiny')
flags.DEFINE_string('model', 'yolov4', 'yolov3 or yolov4')
flags.DEFINE_string('video', './data/video/video.mp4', 'path to input video or set to 0 for webcam')
flags.DEFINE_string('output', None, 'path to output video')
flags.DEFINE_string('output_format', 'XVID', 'codec used in VideoWriter when saving video to file')
flags.DEFINE_float('iou', 0.45, 'iou threshold')
flags.DEFINE_float('score', 0.50, 'score threshold')
# flags.DEFINE_boolean('count', False, 'count objects within video')
flags.DEFINE_boolean('dont_show', False, 'dont show video output')
flags.DEFINE_boolean('info', False, 'print info on detections')
flags.DEFINE_boolean('plate', False, 'perform license plate recognition')
flags.DEFINE_string('street', "university", 'street name')

streets = {
    "university":["city_street",20],
    "airport": ["highway",60],
    "swaileh": ["city_street",30],
    "jordan": ["highway",40],
    "yarmouk": ["highway",40],
    "autostrad": ["highway",45],
    "mecca": ["city_street",25],
    "gardens": ["city_street",30],
    "abu-nusair": ["city_street",30],
    "almadena": ["city_street",47],
    "alsaada": ["city_street",15]
}


sent = 1
def main(_argv):
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)
    STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config(FLAGS)
    input_size = FLAGS.size
    video_path = FLAGS.video
    # get video name by using split method
    video_name = video_path.split('/')[-1]
    video_name = video_name.split('.')[0]
    if FLAGS.framework == 'tflite':
        interpreter = tf.lite.Interpreter(model_path=FLAGS.weights)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        print(input_details)
        print(output_details)
    else:
        saved_model_loaded = tf.saved_model.load(FLAGS.weights, tags=[tag_constants.SERVING])
        infer = saved_model_loaded.signatures['serving_default']

    # begin video capture
    try:
        vid = cv2.VideoCapture(int(video_path))
    except:
        vid = cv2.VideoCapture(video_path)

    out = None

    if FLAGS.output:
        # by default VideoCapture returns float instead of int
        width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(vid.get(cv2.CAP_PROP_FPS))
        codec = cv2.VideoWriter_fourcc(*FLAGS.output_format)
        out = cv2.VideoWriter(FLAGS.output, codec, fps, (width, height))

    frame_num = 0
    while True:
        return_value, frame = vid.read()
        if return_value:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_num += 1
            image = Image.fromarray(frame)
        else:
            print('Video has ended or failed, try a different video format!')
            break
    
        frame_size = frame.shape[:2]
        image_data = cv2.resize(frame, (input_size, input_size))
        image_data = image_data / 255.
        image_data = image_data[np.newaxis, ...].astype(np.float32)
        start_time = time.time()

        if FLAGS.framework == 'tflite':
            interpreter.set_tensor(input_details[0]['index'], image_data)
            interpreter.invoke()
            pred = [interpreter.get_tensor(output_details[i]['index']) for i in range(len(output_details))]
            if FLAGS.model == 'yolov3' and FLAGS.tiny == True:
                boxes, pred_conf = filter_boxes(pred[1], pred[0], score_threshold=0.25,
                                                input_shape=tf.constant([input_size, input_size]))
            else:
                boxes, pred_conf = filter_boxes(pred[0], pred[1], score_threshold=0.25,
                                                input_shape=tf.constant([input_size, input_size]))
        else:
            batch_data = tf.constant(image_data)
            pred_bbox = infer(batch_data)
            for key, value in pred_bbox.items():
                boxes = value[:, :, 0:4]
                pred_conf = value[:, :, 4:]

        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=FLAGS.iou,
            score_threshold=FLAGS.score
        )

        # format bounding boxes from normalized ymin, xmin, ymax, xmax ---> xmin, ymin, xmax, ymax
        original_h, original_w, _ = frame.shape
        bboxes = utils.format_boxes(boxes.numpy()[0], original_h, original_w)

        pred_bbox = [bboxes, scores.numpy()[0], classes.numpy()[0], valid_detections.numpy()[0]]

        # read in all class names from config
        class_names = utils.read_class_names(cfg.YOLO.CLASSES)

        # by default allow all classes in .names file
        allowed_classes = list(class_names.values())
        
        # custom allowed classes (uncomment line below to allow detections for only people)
        #allowed_classes = ['person']


        if True:
            global sent, streets

            # count objects found
            counted_classes = count_objects(pred_bbox, by_class = True, allowed_classes=allowed_classes)
            a = {}
            b = {}
            if 'car' in counted_classes.keys():
                a["car"] = counted_classes['car']
                b['car'] = '{}%'.format(int(counted_classes['car']/streets[FLAGS.street][1]*100))
            else:
                a["car"] = 0
                b['car'] = '0/{}'.format(streets[FLAGS.street][1])
            if 'person' in counted_classes.keys():
                a["person"] = counted_classes['person']
                b["person"] = counted_classes['person']
            else:
                a["person"] = 0
                b["person"] = 0
            # loop through dict and print
            for key, value in a.items():
                print("Number of {}s: {}".format(key, value))
            image = utils.draw_bbox(frame, pred_bbox, FLAGS.info, b, allowed_classes=allowed_classes, read_plate=FLAGS.plate)
        else:
            image = utils.draw_bbox(frame, pred_bbox, FLAGS.info, allowed_classes=allowed_classes, read_plate=FLAGS.plate)
        fps = 1.0 / (time.time() - start_time)
        if streets[FLAGS.street][0] == 'highway':
            if a["car"] and a["person"]:
                if sent <=1 :
                    sent += 1
                    account_sid = "AC3a31353dfb4a548f93229bbd07fe34d1"
                    auth_token = "65753b6a103491b311cd43bf03a92461"
                    client = Client(account_sid, auth_token)
                    call = client.calls.create(
                        twiml=f'<Response><Say>There is a possibility of an accident at {FLAGS.street} street, please check the surveillance Cameras</Say></Response>',
                        to= "+962780146788",
                        from_= "+15055602894"
                    )
                    print(call.sid)
                    
        else:
            if a["car"] >= int(streets[FLAGS.street][1]):
                if FLAGS.video == "0" or FLAGS.video == "1":
                    if sent <=1 :
                        sent += 1
                        account_sid = "AC3a31353dfb4a548f93229bbd07fe34d1"
                        auth_token = "65753b6a103491b311cd43bf03a92461"
                        client = Client(account_sid, auth_token)
                        call = client.calls.create(
                            twiml=f'<Response><Say>you have {a["car"]} cars in {FLAGS.street} street</Say></Response>',
                            to= "+962780146788",
                            from_= "+15055602894"
                        )
                        print(call.sid)

        print("FPS: %.2f" % fps)
        result = np.asarray(image)
        cv2.namedWindow("result", cv2.WINDOW_AUTOSIZE)
        result = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if not FLAGS.dont_show:
            cv2.imshow("result", result)
        
        if FLAGS.output:
            out.write(result)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
