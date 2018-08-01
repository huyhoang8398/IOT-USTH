/* Ket noi giua Raspberry Pi and RPI Sim808 Shield
* RPI Sim808 	|| 		Raspberry Pi
* 	  C_PW		||			GPIO 27
* 	   PWK		|| 			GPIO 17 
*	   TxD 		|| 			RxD (GPIO 15)
* 	   RxD 		|| 			TxD (GPIO 14)
*/

// Compile : gcc -Wall sim808_simple_test.c -o sim808_simple_test -lwiringPi

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>	
#include <signal.h>
#include <unistd.h>
#include <wiringPi.h>
#include <wiringSerial.h>


// Cau hinh GPIO cho Raspberry Pi & RPI Sim808 Shield
const int C_PW_pin = 27;
const int PWK_pin = 17;

/*
* @GSM_Power_On() Bat nguon cho module Sim
*/
void GSM_Power();

/*
* @GSM_Init() Cau hinh cho module sim 
*/
void GSM_Init();

/*
* @GSM_MakeCall() Ham goi dien 
*/
void GSM_MakeCall();

/*
* @GSM_MakeSMS() Ham gui tin nhan 
*/
void GSM_MakeSMS();

/*
* @sig_handler() : ham xu ly ngat ctrl+c
*/
void sig_handler();

int main(void) {

	if(signal(SIGINT, sig_handler) == SIG_ERR)
		printf("\n can't catch \"Ctrl+C\" \n");

	// Setup cac chan GPIO dieu khien module Sim808 
	if (wiringPiSetupGpio() == -1)
  {
    fprintf (stdout, "Unable to start wiringPi: %s\n", strerror (errno)) ;
    return 1 ;
  }
	pinMode(C_PW_pin, OUTPUT);
	pinMode(PWK_pin, OUTPUT);
	

	// Setup UART 
	int fd;
	if((fd = serialOpen ("/dev/ttyAMA0", 9600)) < 0 ){
		fprintf (stderr, "Unable to open serial device: %s\n", strerror (errno));
		return 1;
	};
	// Bat nguon cho module SIM 
	printf("\n\nBat nguon cho module SIM808 ...\n");
	GSM_Power(); 
	// Cau hinh cho Module SIM 808 
	GSM_Init(fd);
	// Test cuoc goi 
	GSM_MakeCall(fd);
	// Test tin nhan
	GSM_MakeSMS(fd);
	// Tat nguon cho module SIM
	printf("Tat nguon cho module SIM808 ...\n");
	GSM_Power();
 
	serialClose(fd); // Close Serial
	digitalWrite(PWK_pin, LOW);
	pinMode(C_PW_pin, INPUT);
	pinMode(PWK_pin, INPUT);

	return 0;
	
}

void GSM_Power(){
	digitalWrite(PWK_pin, HIGH);
	delay(2000);
	digitalWrite(PWK_pin, LOW);
	delay(10000);
	return;
}

void GSM_Init(int fd){
	printf("Khoi tao cho module SIM808...\n");
	serialPuts(fd, "ATE0\r\n"); 			// Tat che do phan hoi (Echo mode)
	delay(2000);
	serialPuts(fd, "AT+IPR=9600\r\n"); 		// Dat toc truyen nhan du lieu 9600 bps
	delay(2000);
	serialPuts(fd, "AT+CMGF=1\r\n");		// Chon che do Text Mode
	delay(2000);
	serialPuts(fd, "AT+CLIP=1\r\n");		// Hien thi thong tin nguoi goi den
	delay(2000);
	serialPuts(fd, "AT+CNMI=2,2\r\n"); 		// Hien thi truc tiep noi dung tin nhan 
	delay(2000);
	return;
}

void GSM_MakeCall(int fd){
	printf("Goi dien...\n");
	serialPuts(fd, "ATD012345678;\r\n"); 	// Goi dien toi sdt 012345678 
	delay(20000);
	serialPuts(fd, "ATH\r\n");
	delay(2000);
	return;
}

void GSM_MakeSMS(int fd){
	printf("Nhan tin...\n");
	serialPuts(fd, "AT+CMGS=\"012345678\"\r\n"); 		// Gui tin nhan toi sdt 012345678
	delay(5000);
	serialPuts(fd, "Xin chao ban!!!");
	serialPutchar(fd, (char)26); 						// Gui Ctrl Z hay 26 de ket thuc noi dung tin nhan va gui di
	delay(5000);
	return;
}

void sig_handler(int signo, int fd){
	if (signo == SIGINT){
		printf("received \"Ctrl+C\" \n");
		serialClose(fd); // Close Serial
		digitalWrite(PWK_pin, LOW);
		pinMode(C_PW_pin, INPUT);
		pinMode(PWK_pin, INPUT);
		exit(0);

	}
	return;
}
