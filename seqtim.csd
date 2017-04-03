<CsoundSynthesizer>
<CsOptions>
-odac:hw:0,0
-+rtaudio=alsa
</CsOptions>
<CsInstruments>

sr = 48000
ksmps = 256
nchnls = 2
0dbfs = 1.0

turnon 12

gkfreq[] fillarray 220, 220, 220, 220
gkcutoff[] fillarray 2000, 2000, 2000, 2000
gkamp init .5
gkrate init 128
gkport = .1
gklforate init 10
gklfodepth init 1
gklfotocutoff init 0
gklfotofreq init 0
gkres init .5
gkatk init 0
gkrel init 0
gkstage init 0

instr 100
;prints "Stage in CSD\n"
gkstage = p4
turnoff
endin


instr 10

gkfreq[0] = p4
gkfreq[1] = p5
gkfreq[2] = p6
gkfreq[3] = p7
gkcutoff[0] = p8
gkcutoff[1] = p9
gkcutoff[2] = p10
gkcutoff[3] = p11
gkrate = p12
gkport = p13 * gkrate / 128.0
gklforate = p14
gklfodepth = p15
gkres = p16
gkatk = p17
gkrel = p18
gklfotocutoff = p19
gklfotofreq = p20

;prints "GKFREQ0: %d", gkfreq[0]

;printks "1: %d, 2: %d, 3: %d, 4: %d\n\n", .1, gkfreq[0], gkfreq[1], gkfreq[2], gkfreq[3]
 
turnoff
endin

instr sequencer
kdetune init .01

kcounter init 0
kstage init 0
klforate init 10
klfodepth init 1

klforate port gklforate, .1, 10
klfodepth port gklfodepth, .1, 1

alfo lfo klfodepth, klforate, 0
kres port gkres, .1, .5

kfreq[] fillarray 220, 220, 220, 220
kcutoff[] fillarray 2000, 2000, 2000, 2000 

kfreq[0] port gkfreq[0], .1, 220
kfreq[1] port gkfreq[1], .1, 220
kfreq[2] port gkfreq[2], .1, 220
kfreq[3] port gkfreq[3], .1, 220

kcutoff[0] port gkcutoff[0], .1, 220
kcutoff[1] port gkcutoff[1], .1, 220
kcutoff[2] port gkcutoff[2], .1, 220
kcutoff[3] port gkcutoff[3], .1, 220

kpfreq portk kfreq[gkstage], gkport, 220

kpcutoff portk kcutoff[gkstage], gkport, 2000

acutoff = kpcutoff

if(gklfotofreq == 1)then
kpfreq += (alfo * kpfreq)
endif

ares lfo .5, kpfreq, 2

if(gklfotocutoff == 1)then
acutoff += (alfo * acutoff)
endif

ares moogladder ares, acutoff, kres

outs ares, ares

endin


</CsInstruments>
<CsScore>
f 0 14400

</CsScore>
</CsoundSynthesizer>
<bsbPanel>
 <label>Widgets</label>
 <objectName/>
 <x>100</x>
 <y>100</y>
 <width>320</width>
 <height>240</height>
 <visible>true</visible>
 <uuid/>
 <bgcolor mode="nobackground">
  <r>255</r>
  <g>255</g>
  <b>255</b>
 </bgcolor>
</bsbPanel>
<bsbPresets>
</bsbPresets>
