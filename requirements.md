# Vision

* What is the vision of this product? the vision for the project is to create a traffic-jam free streets

* What pain point does this project solve? this project is to solve the traffic jam issue, by sending a notification when the traffic reaches a certain capacity

* Why should we care about your product? i think that my project is going to solve a lot of traffic issues, and reduces accidents

## Scope

our project will detect the number of cars on a certain street, and send a message if this street got jammed

### Minimum Viable Product

our Minimum Viable Products are:

Analyze videos or pictures:

1. Detect objects inside the video or the image

2. Achieve a high accuracy in detecting objects

3. Cover as much objects as possible

4. Send an email with the result

### Stretch goals

* create multiple types of models, to detect saved videos and photos

* create a report for the street

### Functional Requirements

* the application can detect the cars properly with high accuracy

* the user can save a copy of this project on his cloud, and run it whenever he wants

#### Data Flow

when the user starts the project, a window of his webcam will start, showing the cars count, if the ratio (cars/max number of cars) reaches a certain point, this will send an email to alert someone about this street

## Non-Functional Requirements

1. using google colab, this will make the testing and developing easier for the model, and it will completely create the project

2. Testing, testing is the most essential part of the project, this will be done whenever the model is ready