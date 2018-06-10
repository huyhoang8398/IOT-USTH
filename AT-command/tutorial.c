#include<SoftwareSerial.h>

SoftwareSerial sim800l(10,11); // (RX,TX)
const String myphone = "01689951815"; // Thay so cua ban vao day

const int RELAY = 12; // Chan so 12 arduino uno dung lam chan dieu khien dong/cat Relay de On/Off
den

String str = ""; // Khai bao bo dem nhan du lieu
// Tat ca du lieu nhan ve tu module sim deu duoc luu trong day

int sms_on = -1; // vi tri cua chuoi "LAMP_ON"
int sms_off = -1; // vi tri cua chuoi "LAMP_OFF"
int call = -1;

void setup() {
    Serial.begin(9600); // Cau hinh UART de giao tiep module Sim 900A
    sim800l.begin(9600); // cổng serial ảo 
    pinMode(RELAY, OUTPUT);
    digitalWrite(RELAY, LOW); // Khai bao chan de dieu khien dong cat RELAY

    delay(10000);
    Gsm_Init(); // Cau hinh module Sim 900A
    Gsm_MakeCall(myphone); // Test cuoc goi 
    Gsm_MakeSMS(myphone,"I'm a test"); // Test tin nhan
}

void loop() {
    delay(10);
    nhan_du_lieu();

    sms_on = str.indexOf("RELAY_ON"); // Tim vi tri cua chuoi "RELAY_ON" trong bo dem nhan str
    sms_off = str.indexOf("RELAY_OFF"); // Tim vi tri cua chuoi "RELAY_OFF" trong bo dem nhan str
    call = str.indexOf(myphone); // có thể thay chữ myphone bằng số điện thoại của bạn ví dụ
    "01689951815"; 
    if(sms_on >= 0) 
    {
	sms_on = -1; // 
	str = ""; // Xoa bo dem
	digitalWrite(RELAY, HIGH); // Dong Relay de bat den // Bat bong den
	Serial.print("da bat den");
    }

    if(sms_off >=0){
	sms_off = -1; 
	str = ""; // Xoa bo dem
	digitalWrite(RELAY, LOW); // Cat Relay de tat den
	Serial.print("da bat den");
    }

    if(call >=0){
	call = -1;
	digitalWrite(RELAY, !digitalRead(RELAY)); // Dong Relay de bat den // Bat bong den
	str = "";
	delay(3000);
	sim800l.println(" ATH");
    }
}
void nhan_du_lieu() { // Chuong trinh ngat nhan du lieu
while (sim800l.available()) { // Doi den khi co du lieu nhan ve
    // get the new byte:
    char inChar = (char)sim800l.read(); // Doc mot byte du lieu vua nhan ve
    str += inChar; // Ghi byte do vao bo dem nhan RxBuff (ta se xu ly RxBuff trong vong loop()) 
}
}

void Gsm_Init()
{
    sim800l.println("ATE0"); // Tat che do phan hoi (Echo mode)
    delay(2000);
    sim800l.println("AT+IPR=9600"); // Dat toc do truyen nhan du lieu 9600 bps
    delay(2000);
    sim800l.println("AT+CMGF=1"); // Chon che do TEXT Mode
    delay(2000);
    sim800l.println("AT+CLIP=1"); // Hien thi thong tin nguoi goi den
    delay(2000);
    sim800l.println("AT+CNMI=2,2"); // Hien thi truc tiep noi dung tin nhan
    delay(2000);
}

void Gsm_MakeCall(String phone) 
{
    sim800l.println("ATD" + phone + ";"); // Goi dien 
    delay(10000); // Sau 10s
    sim800l.println("ATH"); // Ngat cuoc goi
    delay(2000);
}

void Gsm_MakeSMS(String phone,String content)
{
    sim800l.println("AT+CMGS=\"" + phone + "\""); // Lenh gui tin nhan
    delay(3000); // Cho ky tu '>' phan hoi ve 
    sim800l.print(content); // Gui noi dung
    sim800l.print((char)26); // Gui Ctrl+Z hay 26 de ket thuc noi dung tin nhan va gui tin di
    delay(5000); // delay 5s
}
