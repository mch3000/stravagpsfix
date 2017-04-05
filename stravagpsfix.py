# Website: https://github.com/myallh/stravagpsfix

def get_decimal_time(tin):
    a = tin.strip().strip('<time/>Z').split('T')

    d = a[1].split(':')
    dct = float(d[0])*3600+float(d[1])*60+float(d[2])

    return a[0],a[1],dct

def fix_gpx_file(fname=''):
    
    if fname!='':
        txt = 'Reading file '+fname+', press return to accept, or enter a different file name: '
    else:
        txt = 'Enter file name: '
        
    t = raw_input(txt)
    if t!='':
        fname = t
        
    if fname[-4:]!='.gpx':
        raise Exception('Program only reads .gpx files - edit code, or change file extension')
        
    print 'File: '+fname

    lognm = fname[:-4]+'_fixlog.txt'

    log_file = open(lognm,'w')

    ifile = open(fname,'r')

    data = ifile.readlines()

    ifile.close()

    header = []
    footer = []
    points = []

    new_point = False
    head = False  # True when header already read

    for line in data:
        if not new_point:
            # could be a new point, or header, or footer:
            if line[:6]=='<trkpt':
                new_point = True
                points.append([line])
                if not head: head = True
            elif head:
                footer.append(line)
            else:
                header.append(line)

        else:
            points[-1].append(line)
            if line[:8]=='</trkpt>': # end of point data, so new_point reset to False
                new_point = False
                
    # now check points:
    print 'Number of points: ',len(points)
    print 'Check First Point: ',len(points[0])
    
    # first point:

    first_pt = get_decimal_time(points[0][2])

    print 'First Point: ',first_pt

    log_file.write('First Point ')
    log_file.write(points[0][2])


    prev_time = first_pt[2]

    i = 0
    erct = 0 # number of errors in a row
    erls = 0 # number of "large step" errors in a row

    while i < len(points):
        er = False # true if error detected

        if len(points[i][2])!=38:
            er = True
            log_file.write( 'FAILED: TIME FORMAT LENGTH             '+str(i)+'\n')

        if not er:
            vals = get_decimal_time(points[i][2])
            if vals[2]<prev_time:  #if time goes backwards
                log_file.write( 'FAILED: TIME BACKWARDS                 '+str(i)+'\n')
        ##        print 'FAILED: TIME BACKWARDS',i
                er = True
                erls=0 #reset "large step" counter
                log_file.write(  'P '+str(prev_time)+'  C '+str(vals[2])+'\n')
                for k in range(i-1,i+2):
                    if k>=0 and k<len(points):
                        if k==i: log_file.write('--\n')
                        log_file.write( points[k][2])
            elif abs(vals[2]-prev_time)>3.0+erct: # "Large step" error:
                # time step more than 3 seconds + 1 second for each error count (due to intermediate points being removed)
                log_file.write( 'FAILED: LARGE STEP '+str(3+erct).zfill(3)+'                 '+str(i)+'\n')
        ##        print 'FAILED: TIME STEP MORE THAN 10 SECONDS',i
                er = True
                erls+=1
                log_file.write(  'P '+str(prev_time)+'  C '+str(vals[2])+'\n')
                for k in range(i-5,i+5):
                    if k>=0 and k<len(points):
                        if k==i: log_file.write('--\n')
                        log_file.write( points[k][2])

        if erls>10:  # this is probably because there has been a skip in the data, but it is now continuing normally
            log_file.write('****************** erls '+str(erls)+'\n')
            er = False  # so if lots of "large step" errors occur, this means they are ignored (otherwise whole rest of file would be removed)

        if er:
    ##        for v in points[i]:
    ##            print v
    ##        print 'P',prev_time,'  C',vals[2]

            del(points[i])
            erct+=1
            if erct>3:
                log_file.write('****************** erct '+str(erct)+'\n')
        else:
            prev_time = vals[2]
            i+=1
            erct=0
            erls=0
            
    # now write out file:

    ofile = open(fname[:-4]+'_fixed.gpx','wb')

    ofile.writelines(header)

    for p in points:
        ofile.writelines(p)

    ofile.writelines(footer)

    ofile.close()

    log_file.close()

if __name__=='__main__':
    fname = '10102012_pt3.gpx'
    
    fix_gpx_file(fname)
