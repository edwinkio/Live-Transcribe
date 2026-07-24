#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C //Change to 0x3D if the screen doesn't update
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

//4 lines of 20 characters, 4 new lines, and one null terminator
const byte numChars = 85;
byte index = 0;
char receivedChars[numChars];

bool isReceiving = false;
bool newDataReady = false;

void getSentence(void){

  char start = '(';
  char end = ')';
  char currentChar;

  while (Serial.available() && !newDataReady){

      currentChar = Serial.read();

      if (isReceiving){
        if (currentChar != end){
          if (index >= numChars) index = numChars - 1;

          receivedChars[index] = currentChar;
          index++;
        }
        else{
          isReceiving = false;
          receivedChars[index] = '\0';
          index = 0;
          newDataReady = true;
        }
      }
      else if (currentChar == start) isReceiving = true;
    }
}

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10);
  
  //Initialize the display
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE, BLACK);
  display.setTextWrap(true);
}

void loop() {
  
  getSentence();

  if (newDataReady){
    display.clearDisplay();
    display.setCursor(0, 0);
    display.print(receivedChars);
    display.display();

    newDataReady = false;
  }
}