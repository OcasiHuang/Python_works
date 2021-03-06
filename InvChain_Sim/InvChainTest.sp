Lab 1 Problem 1A

* Bring in the library ... 
.lib 'cmoslibrary.lib' nominal

* My VCC is 
.param pvcc = 3

* Sizing Variables
.param alpha = 1.7
.param fan = 7


* Set Power and Ground as Global
.global vcc! gnd!

* AD is the area of the Drain about 1.4u*0.5u
.subckt inv A Z 
  m1 Z A gnd! gnd! nmos w=1.4u l=0.35u  AD=0.7p
  m2 Z A vcc! vcc! pmos w=(1.4u*alpha) l=0.35u AD= 0.7p*alpha
.ends 

*Inverter

Xinv1 a z inv M=1
**Xinv2 b c inv M=fan
**Xinv3 c z inv M=fan*fan
**Xinv4 d e inv M=fan*fan*fan
**Xinv5 e z inv M=fan*fan*fan*fan
**Xinv6 f g inv M=fan*fan*fan*fan*fan
**Xinv7 g z inv M=fan*fan*fan*fan*fan*fan
**Xinv8 h i inv M=fan*fan*fan*fan*fan*fan*fan
**Xinv9 i z inv M=fan*fan*fan*fan*fan*fan*fan*fan
**Xinv10 j k inv M=fan*fan*fan*fan*fan*fan*fan*fan*fan
**Xinv11 k z inv M=fan*fan*fan*fan*fan*fan*fan*fan*fan*fan
Cload z gnd! 5pF

Vin a gnd! 0V PWL 0 0NS 1NS 3 20NS 3


.measure TRAN tphl_inv  TRIG v(Xinv1.a) VAL = 1.5 RISE = 1 TARG v(Xinv1.z) VAL=1.5 FALL = 1

* Power Supplies
Vgnd gnd! 0 DC = 0
Vvcc vcc! 0 DC = 3V

* Analysis
.tran 1NS 40NS
.print tran v(a) v(z)

.OPTION MEASFORM=3

.OPTION POST
.TEMP 25 

.end
