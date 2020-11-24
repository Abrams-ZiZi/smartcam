#define LED1 9
#define LED2 10
#define LED3 11
#define LED4 12
#define LED5 13

#include <Servo.h>

Servo myservo1;
Servo myservo2;

void setup() {
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  pinMode(LED4, OUTPUT);
  pinMode(LED5, OUTPUT);
  myservo1.attach(8);
  myservo2.attach(7);
  Serial.begin(9600);
}

void loop() {
  GatewaycommunicatingStatemachine();
  delay(5);
  faceCountStateMachine();
  delay(5);
}

void moveRight() {
  if (myservo1.read() > 0) {
    myservo1.write(myservo1.read() - 5);
  }
}

void moveLeft() {
  if (myservo1.read() < 180) {
    myservo1.write(myservo1.read() + 5);
  }
}

void moveUp() {
  if (myservo2.read() > 0) {
    myservo2.write(myservo2.read() - 5);
  }
}

void moveDown() {
  if (myservo2.read() < 180) {
    myservo2.write(myservo2.read() + 5);
  }
}

void setPosition(int x, int y) {
  myservo1.write(x);
  myservo2.write(y);
}
