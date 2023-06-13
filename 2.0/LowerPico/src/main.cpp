// подключаем библиотеки 
#include <Arduino.h>
#include <Servo.h>
#include <GParser.h>
#include <AsyncStream.h>
#include <ServoSmooth.h>
#include <Config.h>
#include <GyverFilters.h>


ServoSmooth servos[8];
AsyncStream<100> serial(&Serial, '\n');
// TODO подобрать параметры измерения вольтажа
GKalman testFilter(10, 10, 0.1);
uint32_t turnTimer;


void setup() {
  // подключение отладочного сериала 
  Serial.begin(115200);

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

  delay(3000);

}

void loop() {
  if (millis()- turnTimer >= 20){
    turnTimer = millis();
    servos[0].tick();
    servos[1].tick();
    servos[2].tick();
    servos[3].tick();
    servos[4].tick();
    servos[5].tick();
    servos[6].tick();
    servos[7].tick();
  }
    
  // если данные получены
  if (serial.available()) {
    // парсим данные по резделителю возвращает список интов 
    GParser data = GParser(serial.buf, ' ');
    if (DEBUG) Serial.println(serial.buf);
    int data_input[data.amount()];
    int am = data.parseInts(data_input);

    // отправляем значения на микроконтроллер 
    int motor_0_out = 1000 + (data_input[0] * 10);
    int motor_1_out = 1000 + (data_input[1] * 10);
    int motor_2_out = 1000 + (data_input[2] * 10);
    int motor_3_out = 1000 + (data_input[3] * 10);
    int motor_4_out = 1000 + (data_input[4] * 10);
    int motor_5_out = 1000 + (data_input[5] * 10);
    int motor_6_out = 1000 + (data_input[6] * 10);
    int motor_7_out = 1000 + (data_input[7] * 10);

    servos[0].setTarget(motor_0_out);
    servos[1].setTarget(motor_1_out);
    servos[2].setTarget(motor_2_out);
    servos[3].setTarget(motor_3_out);
    servos[4].setTarget(motor_4_out);
    servos[5].setTarget(motor_5_out);
    servos[6].setTarget(motor_6_out);
    servos[7].setTarget(motor_7_out);

    // отправка вольтажа на пост управления 
    if (DEBUG) Serial.println(testFilter.filtered(analogRead(28)));
  }  
}
