# serumwt2fathom
This python script will convert Serum wavetables so they can be used in
Fathom Synth. Fathom wavetables are currently limited to 16 waveforms. If a 
Serum wavetable contains more than 16 waveforms, serumwt2fathom will 
select an even distribution of waveforms from the Serum wavetable. For
example, if a Serum wavetable contains 32 waveforms, then every odd 
numbered waveform will be selected. If a Serum wavetable contains less
than 16 waveforms. then consecutive Fathom slots are fill with the Serum
waveforms.

Then script is strictly command line; no fancy GUI is provided. Usage is

python serumwt2fathom \<path-to-serum-wavetable\>

Provided all goes well,a fathom wavetable will be created in the same 
folder containing the serum wavetable. The Fathom wavetable can then be
copied to the appropriate Fathom wavetable folder and used as is in 
Fathom.
