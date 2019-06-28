#!/usr/bin/env python3
#
import sys
import os
import soundfile as sf
from chunk import Chunk
    
def getSamplesPerWave(fullfilename):   
    with open(fullfilename, 'rb') as wavfile:
        rootchunk = Chunk(wavfile, bigendian = False)
        if rootchunk.getname() != b'RIFF':
            raise RuntimeError('not a RIFF file')
        if rootchunk.read(4) != b'WAVE':
            raise RuntimeError('not a WAVE file')
        
        samplesperwav=0
        clmfound= False
        while True:
            try:
                riffchunk = Chunk(rootchunk, bigendian = 0)
            except EOFError:
                break
            
            chunkname = riffchunk.getname()
            
            if chunkname == b'clm ':
                clmfound = True
                if riffchunk.read(3) != b'<!>':
                    raise Error('not a Serum wavetable')
                samplesperwav=int(riffchunk.read(4))
                
                break;
                
            riffchunk.skip()
            
    if not clmfound:
        raise RuntimeError('not a Serum wavetable')
    return samplesperwav

if __name__ == "__main__":
    wavetablefile=sys.argv[1]
    
    try:
        samplesperwave = getSamplesPerWave(wavetablefile)
    except (RuntimeError, IOError) as err:
        sys.stderr.write('ERROR: %s\n' % str(err))
        exit(1)

    filename, fileextension = os.path.splitext(wavetablefile)

    data, samplerate = sf.read(wavetablefile)
        
    nwaveforms=int(data.shape[0]) / samplesperwave


    with open(filename+".Wave Table.xml", "w") as of:
        of.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        of.write("<SynthWaveTable Name=\"Wave 1\">\n")
        of.write("  <WaveTable>\n")

        serumwfindex = 0
        waveformfloatindex = 0.0
        fathonwfindex = 0
        waveformstep = nwaveforms / 16.0
        while serumwfindex < nwaveforms:
            of.write("    <wave>\n")
#            of.write("      <Members ObjectIdNumber=\"10\" TableX=\"0\" TableY=\""+str(fathonwfindex)+\"/>\n")
            of.write("      <Members ObjectIdNumber=\"10\" TableX=\"0\" TableY=\""+str(fathonwfindex)+"\" SerumWaveformIndex=\""+str(serumwfindex)+"\"/>\n")
            of.write("      <Buffer>\n")
            of.write("        <Members NumSamples=\""+str(samplesperwave)+"\" Size=\""+str(samplesperwave)+"\" SizeAllocated=\""+str(samplesperwave)+"\" Index=\"0\" IsDoubleSize=\"0\"/>\n")
            of.write("        <Samples>")
            for sampleindex in range(0, samplesperwave):
                if sampleindex < samplesperwave-1:
                    of.write(str(data[serumwfindex*samplesperwave+sampleindex]))
                    of.write(", ")
                else:
                    of.write(str(data[serumwfindex*samplesperwave+sampleindex]))
            
            of.write("</Samples>\n")
            of.write("      </Buffer>\n")
            of.write("    </wave>\n")
            fathonwfindex+=1
            if nwaveforms < 17:
                serumwfindex+=1
            else:
                waveformfloatindex+= waveformstep
                serumwfindex = int(round(waveformfloatindex))
                    
        of.write("  </WaveTable>\n")
        of.write("</SynthWaveTable>\n")
