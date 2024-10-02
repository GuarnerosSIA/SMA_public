#include <Wire.h>
#include <Adafruit_MLX90614.h>
#include "Adafruit_VL53L0X.h"



Adafruit_MLX90614 mlx = Adafruit_MLX90614();
Adafruit_MLX90614 mlx2 = Adafruit_MLX90614();
Adafruit_VL53L0X lox = Adafruit_VL53L0X();


int IN2 = 5;
int IN3 = 6;

int trash = 0;
int rec[10];

int PWM_A = 0;
int PWM_A_basura = 0;

int PWM_B = 0;
int PWM_B_basura = 0;

float temperatura_SMA_A = 0.0;
float temperatura_amb_A = 0.0;

float temperatura_SMA_B = 0.0;
float temperatura_amb_B = 0.0;

float distancia = 0.0;


// Comunicacion serial
int cont = 0;
int safe = 0;

void setup() 
{
  pinMode(IN2,OUTPUT);
  pinMode(IN3,OUTPUT);
  pinMode(13,OUTPUT);

  
  digitalWrite(IN3,LOW);
  digitalWrite(IN2,LOW);
  digitalWrite(13,LOW);
  
  Serial.begin(115200);  
  mlx.begin(0x5A);
  mlx2.begin(0x5B);
  lox.begin();
  
}

void loop() 
{
  // put your main code here, to run repeatedly:
  VL53L0X_RangingMeasurementData_t distancia;
  if(Serial.available()>0)
  {
    trash = Serial.read();
    if (trash == 'x'){
      for(int i=0; i<=10; i++){
        if(Serial.available()>0){
          rec[i] = Serial.read()-48;
          }
        }

        lox.rangingTest(&distancia, false);
        PWM_A_basura = PWM_A;
        PWM_A = rec[0]*10000+rec[1]*1000+rec[2]*100+rec[3]*10+rec[4];
        PWM_A -= 10000;

        // Esto es para que el PWM se mantenga dentro de valores correctos
        if (PWM_A > 255 || PWM_A < 0)
        {
          PWM_A = 0;
        }

        PWM_B_basura = PWM_B;
        PWM_B = rec[5]*10000+rec[6]*1000+rec[7]*100+rec[8]*10+rec[9];
        PWM_B -= 10000;

        if (PWM_B > 255 || PWM_B < 0)
        {
          PWM_B = 0;
        }

        temperatura_SMA_A = mlx.readObjectTempC();
        temperatura_amb_A = mlx.readAmbientTempC();

        temperatura_SMA_B = mlx2.readObjectTempC();
        temperatura_amb_B = mlx2.readAmbientTempC();
        
      safe = 0;

      analogWrite(IN2,PWM_A);
      analogWrite(IN3,PWM_B);
      analogWrite(13,PWM_A);  
      Serial.print(temperatura_amb_A);
      Serial.print(",");
      Serial.print(temperatura_amb_B);
      Serial.print(",");
      Serial.print(PWM_A);
      Serial.print(",");
      Serial.print(PWM_B);
      Serial.print(",");
      Serial.print(temperatura_SMA_A);
      Serial.print(",");
      Serial.print(temperatura_SMA_B);
      Serial.print(",");
      
    if (distancia.RangeStatus != 4)
    {
      Serial.println(distancia.RangeMilliMeter);
    } 
    else
    {
      Serial.println(-1);
    }
    
    }
  }
  safe += 1;
  if(safe > 50){
    analogWrite(IN2,0);
    analogWrite(IN3,0);
    analogWrite(13,0);
    }
    
  delay(30);
}
