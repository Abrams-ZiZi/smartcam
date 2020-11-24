#define stdby  0
#define processing 10
#define awaitcommand 30
#define awaitparameter 40
#define awaitvalue 50
#define awaitend 60

char Command, Parameter, Value1, Value2;


int ComState = stdby;


void  GatewaycommunicatingStatemachine() {
  int x ;
  if ((x = Serial.read ()) == -1)  return ;
  switch (ComState) {
    case stdby:
      if (x == ':') ComState = awaitcommand;
      break;
    case awaitcommand:
      if (x == 'M' || x == 'R' || x == 'S')
      {
        ComState = awaitparameter;
        Command = x;
      }
      else if (x == '@')
      {
        ComState = awaitend;
        Command = x;
      }
      else
      {
        ComState = stdby;
      }
      break;
    case awaitparameter:
      if (x == 'R' || x == 'L' || x == 'U' || x == 'D' || x == 'P' || x == 'F')
      {
        Parameter = x;
        if (Command == 'S')
        {
          ComState = awaitvalue;
        }
        else //Command == R   --- Read
        {
          ComState = awaitend;
        }
      }
      else
      {
        ComState = stdby;
      }
      break;
    case awaitvalue:
      //Serial.println("Value acceptrd\n");
      //Serial.println(x);
      Value1 = x;
      if (Parameter == 'P') {
        Value2 = Serial.read();
      }
      ComState = awaitend;   ////
      break;
    case awaitend:
      if (x == '\r')
      {
        ComState = stdby;
        ProcesPacket();
      }
      break;
  }
  //Serial.print("\nComstate");
  //Serial.println(ComState);
}

void ProcesPacket(void)
{
  //Serial.println("Processing packet \nCommand :");
  //Serial.println(Command);

  if (Command == '@')
  {
    Serial.print('@');
  }
  if (Command == 'M')
  {
    //Serial.println("MOVE");
    switch (Parameter) {
      case 'R' :
        moveRight();
        break;
      case 'L' :
        moveLeft();
        break;
      case 'U' :
        moveUp();
        break;
      case 'D' :
        moveDown();
        break;
    }
  }

  if (Command == 'R') {
    if (Parameter == 'P') {
      Serial.write(myservo1.read());
      Serial.write(myservo2.read());
    }
    if (Parameter == 'F') {
      Serial.write(faceCount);
    }
  }

  if (Command == 'S') {
    if (Parameter == 'P') {
      //Serial.println("Seting position \n");
      //Serial.println(Value1);
      //Serial.println(Value2);
      setPosition(Value1, Value2);
    }
    else if (Parameter == 'F') {
      //Serial.println("Updating face count \n");
      faceCount = Value1;
    }
  }
}
