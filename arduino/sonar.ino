#include <NewPing.h>
 
#define TRIGGER_PIN_FRONT  2
#define ECHO_PIN_FRONT     3

#define MAX_DISTANCE 500
#define PING_MEDIAN 3

NewPing sonarFront(TRIGGER_PIN_FRONT, ECHO_PIN_FRONT, MAX_DISTANCE);

int sonarFrontGetDistance() {
  return sonarFront.convert_cm(sonarFront.ping_median(PING_MEDIAN));
}
