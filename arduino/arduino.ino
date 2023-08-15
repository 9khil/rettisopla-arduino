#include "Adafruit_seesaw.h"
#include <Keyboard.h>
#include <seesaw_neopixel.h>
#include <debounce.h> //by Aaron Kimball

#define  ARCADE_BOARD_1 0x3A
#define  ARCADE_BOARD_2 0x3B

//Board 1
#define  CLEAR  18 // Switch 1
#define  CLEAR_LED_PWM  12

#define  RED  19 // Switch 2
#define  RED_LED_PWM  13

#define  YELLOW  20  //Switch 3
#define  YELLOW_LED_PWM  0

#define  BLUE  2 // Switch 4
#define  BLUE_LED_PWM  1

//Board 2
#define  GREEN  18 // Switch 5 (Board 2, switch 1)
#define  GREEN_LED_PWM  12


Adafruit_seesaw ss;
Adafruit_seesaw ss2;

static void buttonHandlerBoard2(uint8_t btnId, uint8_t btnState) {
  if(btnState == BTN_PRESSED) {
    switch(btnId){
        case GREEN:
          Serial.println("GREEN");
          Keyboard.write('t');
          ss2.analogWrite(GREEN_LED_PWM, 0);
          break;  
    }
  }else{
    switch(btnId){
        case GREEN:
          ss2.analogWrite(GREEN_LED_PWM, 255);
          break;
    }
  }
}
static void buttonHandler(uint8_t btnId, uint8_t btnState) {
  if (btnState == BTN_PRESSED) {

    switch(btnId){
      case CLEAR:
        Serial.println("CLEAR");
        Keyboard.write('q');
        ss.analogWrite(CLEAR_LED_PWM, 0);
        break;
      case RED:
        Serial.println("RED");
        Keyboard.write('w');
        ss.analogWrite(RED_LED_PWM, 0);
        break;
      case YELLOW:
        Serial.println("YELLOW");
        Keyboard.write('e');
        ss.analogWrite(YELLOW_LED_PWM, 0);
        break;
      case BLUE:
        Serial.println("BLUE");
        Keyboard.write('r');
        ss.analogWrite(BLUE_LED_PWM, 0);
        break;
      default:
        Serial.println("Unknown button pushed");
    }

  }else{
    switch(btnId){
      case CLEAR:
        ss.analogWrite(CLEAR_LED_PWM, 255);
        break;
      case RED:
        ss.analogWrite(RED_LED_PWM, 255);
        break;
      case YELLOW:
        ss.analogWrite(YELLOW_LED_PWM, 255);
        break;
      case BLUE:
        ss.analogWrite(BLUE_LED_PWM, 255);
        break;
    }
  }
}

static Button clearButton(CLEAR, buttonHandler);
static Button redButton(RED, buttonHandler);
static Button yellowButton(YELLOW, buttonHandler);
static Button blueButton(BLUE, buttonHandler);

static Button greenButton(GREEN, buttonHandlerBoard2);

void setup() {
  Serial.begin(115200);

  Serial.println(F("Rett i søpla! Running setup"));
  
  Keyboard.begin();

  if (!ss.begin(ARCADE_BOARD_1)) {
    Serial.println(F("1x4 arcade button board 1 not found!"));
    while(1) delay(10);
  }

  if(!ss2.begin(ARCADE_BOARD_2)){
    Serial.println(F("1x4 arcade button board 2 not found!"));
    while(1) delay(10);
  }

  uint16_t pid;
  uint8_t year, mon, day;
  ss.getProdDatecode(&pid, &year, &mon, &day);  
  Serial.println("seesaw found PID: ");
  Serial.print(pid);

  if (pid != 5296) {
    Serial.println(F("Wrong seesaw PID"));
    while (1) delay(10);
  }


  ss2.getProdDatecode(&pid, &year, &mon, &day);
  Serial.println("---------SeeSaw board 2--------");
  Serial.println("seesaw found PID: ");
  Serial.print(pid);

  if (pid != 5296) {
    Serial.println(F("Wrong seesaw PID"));
    while (1) delay(10);
  }

  Serial.println(F("seesaw started OK!"));
  ss.pinMode(CLEAR, INPUT_PULLUP);
  ss.pinMode(RED, INPUT_PULLUP);
  ss.pinMode(YELLOW, INPUT_PULLUP);
  ss.pinMode(BLUE, INPUT_PULLUP);
  
  ss2.pinMode(GREEN, INPUT_PULLUP);
 
  
  ss.analogWrite(CLEAR_LED_PWM, 0);//turn all LEDS off
  ss.analogWrite(RED_LED_PWM, 0);
  ss.analogWrite(YELLOW_LED_PWM, 0); 
  ss.analogWrite(BLUE_LED_PWM, 0);
  
  ss2.analogWrite(GREEN_LED_PWM, 0);

  delay(500);

  ss.analogWrite(CLEAR_LED_PWM, 255);
  delay(500);
  ss.analogWrite(RED_LED_PWM, 255);
  delay(500);
  ss.analogWrite(YELLOW_LED_PWM, 255); //Default value LED lit up
  delay(500);
  ss.analogWrite(BLUE_LED_PWM, 255);
  delay(500);
  ss2.analogWrite(GREEN_LED_PWM, 255);
  
  Serial.println("Setup done!");
  delay(1000);
}

static void pollButtons() {
  clearButton.update(ss.digitalRead(CLEAR));
  redButton.update(ss.digitalRead(RED));
  yellowButton.update(ss.digitalRead(YELLOW));
  blueButton.update(ss.digitalRead(BLUE));
  greenButton.update(ss2.digitalRead(GREEN));
}

void loop() {
  pollButtons();
  delay(10); 
}
