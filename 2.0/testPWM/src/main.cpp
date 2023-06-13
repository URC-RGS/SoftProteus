#include <Arduino.h>
#include <GParser.h>
#include <ServoSmooth.h>
#include <AsyncStream.h>

#include <Config.h>


ServoSmooth servos[10];
AsyncStream<50> serial(&Serial, '\n');
uint32_t servoTimer;

void setup() {
  Serial.begin(57600);
  
  // подключаем
  servos[0].attach(PIN_MOTOR_0, 1000, 2000);
  servos[0].setSpeed(SPEED_MOTOR);
  servos[0].setAccel(ACCELERATE_MOTOR);
  servos[0].setTarget(1500);
  servos[0].setAutoDetach(false);

  servos[1].attach(PIN_MOTOR_1, 1000, 2000);
  servos[1].setSpeed(SPEED_MOTOR);
  servos[1].setAccel(ACCELERATE_MOTOR);
  servos[1].setTarget(1500);
  servos[1].setAutoDetach(false);

  servos[2].attach(PIN_MOTOR_2, 1000, 2000);
  servos[2].setSpeed(SPEED_MOTOR);
  servos[2].setAccel(ACCELERATE_MOTOR);
  servos[2].setTarget(1500);
  servos[2].setAutoDetach(false);

  servos[3].attach(PIN_MOTOR_3, 1000, 2000);
  servos[3].setSpeed(SPEED_MOTOR);
  servos[3].setAccel(ACCELERATE_MOTOR);
  servos[3].setTarget(1500);
  servos[3].setAutoDetach(false);

  servos[4].attach(PIN_MOTOR_4, 1000, 2000);
  servos[4].setSpeed(SPEED_MOTOR);
  servos[4].setAccel(ACCELERATE_MOTOR);
  servos[4].setTarget(1500);
  servos[4].setAutoDetach(false);

  servos[5].attach(PIN_MOTOR_5, 1000, 2000);
  servos[5].setSpeed(SPEED_MOTOR);
  servos[5].setAccel(ACCELERATE_MOTOR);
  servos[5].setTarget(1500);
  servos[5].setAutoDetach(false);

  servos[6].attach(PIN_MOTOR_6, 1000, 2000);
  servos[6].setSpeed(SPEED_MOTOR);
  servos[6].setAccel(ACCELERATE_MOTOR);
  servos[6].setTarget(1500);
  servos[6].setAutoDetach(false);

  servos[7].attach(PIN_MOTOR_7, 1000, 2000);
  servos[7].setSpeed(SPEED_MOTOR);
  servos[7].setAccel(ACCELERATE_MOTOR);
  servos[7].setTarget(1500);
  servos[7].setAutoDetach(false);

  servos[8].attach(PIN_SERVO_CAM, 1000, 2000);
  servos[8].setSpeed(SPEED_SERVO);
  servos[8].setAccel(ACCELERATE_SERVO);
  servos[8].setTarget(1500);
  servos[8].setAutoDetach(false);

  servos[9].attach(PIN_SERVO_ARM, 1000, 2000);
  servos[9].setSpeed(SPEED_SERVO);
  servos[9].setAccel(ACCELERATE_SERVO);
  servos[9].setTarget(1500);
  servos[9].setAutoDetach(false);
}


void loop() {
  // каждые 20 мс
  if (millis() - servoTimer >= 20) {  // взводим таймер на 20 мс (как в библиотеке)
    servoTimer += 20;
    for (byte i = 0; i < 8; i++) {
      servos[i].tickManual();   // двигаем все сервы. Такой вариант эффективнее отдельных тиков
    }
  } 

  if (serial.available()) {     // если данные получены
    GParser data = GParser(serial.buf, ' ');
    int am = data.split();
    if (am == 2) {
      int pin = data.getInt(0);
      int pwm_out = data.getInt(1);
      if (pin > -1 and pin < 10 and pwm_out > 999 and pwm_out < 2001){
        Serial.print("Output: ");
        Serial.print(data.getInt(0));
        Serial.print(" PWM: ");
        Serial.println(data.getInt(1));
        // непосредственно подача шим на указанный пин
        servos[pin].setTarget(pwm_out);} 

      else Serial.println("Error");
      }
    else Serial.println("Error"); 
  }
}


// #include <Servo.h>

// Servo myservo;  // create servo object to control a servo
// // twelve servo objects can be created on most boards

// int pos = 0;    // variable to store the servo position

// void setup() {
//   myservo.attach(3);  // attaches the servo on pin 9 to the servo object
// }

// void loop() {
//   for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
//     // in steps of 1 degree
//     myservo.write(pos);              // tell servo to go to position in variable 'pos'
//     delay(15);                       // waits 15 ms for the servo to reach the position
//   }
//   for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
//     myservo.write(pos);              // tell servo to go to position in variable 'pos'
//     delay(15);                       // waits 15 ms for the servo to reach the position
//   }
// }