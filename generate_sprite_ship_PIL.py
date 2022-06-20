#import sys
import math
import os
import random
from PIL import Image

def remap(value, fromLow, fromHigh, toLow, toHigh): 
    return (value - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow

def avg_deviation(numlist):
    totalnum = 0
    for num in numlist:
        totalnum += num
    avg = totalnum/len(numlist)
    x = 0
    for num in numlist:
        x += (num-avg)**2
    return avg, math.sqrt(x/totalnum)

#TODO: Train AI for generating parts to be assembled.
def get_sprites(setselect="human"):
    #print(os.listdir(f"imgparts/{setselect}"))
    file_list = [f for f in os.listdir(f"imgparts/{setselect}") if f.endswith(".png") or f.endswith(".PNG")]
    part_directional = [] #unsorted directional part
    part_non_directional = [] #unsorted non-directional part

    #Create catalog, assembly required before use.
    for part in file_list:
        part = part.removesuffix(".png")
        part = part.removesuffix(".PNG")
        #print("cata:", part)
        if part.endswith("-l") or part.endswith("-r"):
            if part.endswith("-l"): #if -l exist -r also should, handle later if not.
                part = part.removesuffix("-l")
                part_directional.append(part)
                #print("dir:", part)
        else:
            part_non_directional.append(part)
            #print("uni:", part)
    part_dir_dict = {}
    part_dir_dict['engine'] = []
    part_dir_dict['gun'] = []
    part_dir_dict['turret'] = []
    part_dir_dict['perimeter'] = []
    part_dir_dict['cockpit'] = []
    part_dir_dict['body'] = []
    part_dir_dict['core'] = []
    part_dir_dict['greeble'] = []
    part_dir_dict['other'] = []
    #sort by catagory
    for part in part_directional:
        part = f"imgparts/{setselect}/"+part
        if part.endswith("engine"):
            part_dir_dict['engine'].append(part)
        elif part.endswith("gun"):
            part_dir_dict['gun'].append(part)
        elif part.endswith("turret"):
            part_dir_dict['turret'].append(part)
        elif part.endswith("perimeter"):
            part_dir_dict['perimeter'].append(part)
        elif part.endswith("cockpit"):
            part_dir_dict['cockpit'].append(part)
        elif part.endswith("body"):
            part_dir_dict['body'].append(part)
        elif part.endswith("core"):
            part_dir_dict['core'].append(part)
        elif part.endswith("greeble"):
            part_dir_dict['greeble'].append(part)
        else:
            part_dir_dict['other'].append(part)
    
    part_uni_dict = {}
    part_uni_dict['engine'] = []
    part_uni_dict['gun'] = []
    part_uni_dict['turret'] = []
    part_uni_dict['perimeter'] = []
    part_uni_dict['cockpit'] = []
    part_uni_dict['body'] = []
    part_uni_dict['core'] = []
    part_uni_dict['greeble'] = []
    part_uni_dict['other'] = []
    for part in part_non_directional:
        part = f"imgparts/{setselect}/"+part
        if part.endswith("engine"):
            part_uni_dict['engine'].append(part)
        elif part.endswith("gun"):
            part_uni_dict['gun'].append(part)
        elif part.endswith("turret"):
            part_uni_dict['turret'].append(part)
        elif part.endswith("perimeter"):
            part_uni_dict['perimeter'].append(part)
        elif part.endswith("cockpit"):
            part_uni_dict['cockpit'].append(part)
        elif part.endswith("body"):
            part_uni_dict['body'].append(part)
        elif part.endswith("core"):
            part_uni_dict['core'].append(part)
        elif part.endswith("greeble"):
            part_uni_dict['greeble'].append(part)
        else:
            part_uni_dict['other'].append(part)
    return part_dir_dict,part_uni_dict

def pick_part_dir (partDir): #TODO: check and choose appropriate sprite size for category.
    #random.shuffle(partlistdir)
    #print("Dir")
    #note parts already got directory attached.
    try:
        Image.open(partDir+"-r.png")
        Lexist = True
    except FileNotFoundError:
        Lexist = False
    try:
        Image.open(partDir+"-l.png")
        Rexist = True
    except FileNotFoundError:
        Rexist = False
    #print(Lexist,Rexist)
    if Lexist and Rexist:
        part_suffix_l = "-l.png"
        part_suffix_r = "-r.png"
        part = [Image.open(partDir+part_suffix_l),
                Image.open(partDir+part_suffix_r)]
    elif Lexist and not Rexist:
        part_suffix_l = "-l.png"
        part_suffix_r = "-l.png"
        part = [Image.open(partDir+part_suffix_l),
                Image.open(partDir+part_suffix_l)]
    elif Rexist and not Lexist:
        part_suffix_l = "-r.png"
        part_suffix_r = "-r.png"
        part = [Image.open(partDir+part_suffix_r),
                Image.open(partDir+part_suffix_r)]
    return part

#Get valid range of positions
def get_part_pos (partlist,newboundmin,newboundmax,mode,part,part_size,uniMode,stray=[[1,1],[1,1]],core_img=None):
    if mode.casefold() == 'x':
        mode_sel = 0
    else:
        mode_sel = 1
    valid_part = False
    h = 0
    while not valid_part:
        h += 1
        m = random.randrange(len(newboundmin)) #TODO: Center mode filtering.
        #print(f"bminmax {mode}:",newboundmin[m][mode_sel],newboundmax[m][mode_sel])
        for n in partlist:
            if mode_sel == 0:
                rposmin = round(newboundmin[m][0]*stray[0][0])
                rposmax = round((newboundmax[m][0]*stray[0][1]))
                canvasmin = abs(part_size[0][mode_sel]/2)
                canvasmax = (core_img.size[0])-part_size[0][mode_sel]*.5
                #print(f"TrueImg:    {core_img.size[0],core_img.size[1]}")
                #print(f"Compensated:{canvasmin,canvasmax}")
                #print(f"PrevBoundX: {rposmin,rposmax}")
                rposmin = max(rposmin,canvasmin)
                rposmax = min(rposmax,canvasmax)
                #print(f"NewBoundX:  {rposmin,rposmax}")
            else:
                #rposmax = round(newboundmax[m][mode_sel]-abs(part_size[0][mode_sel]/2-core_img.size[0]))
                #rposmin = round(newboundmin[m][mode_sel]+abs(part_size[0][mode_sel]/2-core_img.size[0]))
                rposmin = round(newboundmin[m][mode_sel]*stray[1][0])
                rposmax = round(newboundmax[m][mode_sel]*stray[1][1]) 
                canvasmin = abs(part_size[0][mode_sel])
                canvasmax = (core_img.size[1])-part_size[0][mode_sel]*.5
                #print(f"TrueImg:    {core_img.size[0],core_img.size[1]}")
                #print(f"Compensated:{canvasmin,canvasmax}")
                #print(f"PrevBoundY: {rposmin,rposmax}")
                rposmin = max(rposmin,canvasmin)
                rposmax = min(rposmax,canvasmax)
                #print(f"NewBoundY:  {rposmin,rposmax}")
            #If it doesn't fit, pick a new part.
            if rposmin < rposmax: 
                valid_part = True
                break
            else:
                if not uniMode:
                    part = pick_part_dir(n)
                    part_size = [p.size for p in part]
                else:
                    part = Image.open(n+".png")
                    part = [part, part]  
                    part_size = [p.size for p in part]
        
        #If no part fits, rescale the part. Low Pri as some part might not work well resized.
        if not valid_part:
            nscale = .9
            for n in range(part_size[0][mode_sel]-1):
                #part[L/R][X/Y]
                new_size = [max(1,math.ceil(part[0].size[0] * nscale)),max(1,math.ceil(part[0].size[1] * nscale))]
                part = [p.resize(new_size) for p in part]
                part_size = [p.size for p in part]
                rposmin = round(newboundmin[m][mode_sel])
                rposmax = round(newboundmax[m][mode_sel])
                rposmin = max(rposmin,abs(part_size[0][mode_sel]/2))
                rposmax = min(rposmax,((core_img.size[mode_sel]/2)*1+mode_sel)-part_size[0][mode_sel]/2)
                canvasmin = abs((part_size[0][mode_sel]/2)*1+mode_sel)
                canvasmax = (core_img.size[mode_sel])-part_size[0][mode_sel]*.5
                rposmin = max(rposmin,canvasmin)
                rposmax = min(rposmax,canvasmax)
                if rposmin > rposmax:
                    nscale -= .1
                else:
                    valid_part = True
                    break
        if valid_part:
            break
        if h >= 100:
            part = [Image.new('RGBA',[1,1],'black') for i in range(2)]
            part_size = [p.size for p in part]
            if mode_sel == 0:
                rposmin = round(newboundmin[m][0]*stray[0][0])
                rposmax = round((newboundmax[m][0]*stray[0][1]))
                canvasmin = abs(part_size[0][mode_sel]/2)
                canvasmax = (core_img.size[0])-part_size[0][mode_sel]*.5
                rposmin = max(rposmin,canvasmin)
                rposmax = min(rposmax,canvasmax)   
            else:
                rposmin = round(newboundmin[m][mode_sel]*stray[1][0])
                rposmax = round(newboundmax[m][mode_sel]*stray[1][1]) 
                canvasmin = abs(part_size[0][mode_sel])
                canvasmax = (core_img.size[1])-part_size[0][mode_sel]*.5
                rposmin = max(rposmin,canvasmin)
                rposmax = min(rposmax,canvasmax)
            break
    #print(f"bminmax {mode}:",newboundmin[m][mode_sel],newboundmax[m][mode_sel])
    return part,part_size,rposmin,rposmax

def place_parts(core_img,
               part_list,
               count,
               symmetric=True,
               center=False,
               part_type='random',
               boundmin=[0,0],
               boundmax=[0,0],
               dir_chance = .5,
               weightX = .3,
               scaleRange = [1,1],
               pattern=None,
               clustermode = False,
               bounddict={},
               inputdictonly=False):

    width,height = core_img.size
    centW = round(width/2)
    centH = round(height/2)
    weightXAsym = weightX*2
    if boundmax == [0,0]:
        boundmax = core_img.size
    count = round(count)

    #print("DictIn:",bounddict)
    part_dir_dict = part_list[0]
    part_uni_dict = part_list[1]

    bound_constrainX = .75
    bound_constrainY = 1 #Don't go below engine_min_H
    bound_minX = .8
    bound_minY = .8
    engine_min_H = .7
    gun_max_H = .2 #def .5
    gun_max_W = .2
    straypercentX = 1
    straypercentY = 1
    #=============================PART SELECTION
    haveparts = False
    if part_type == 'random':
        while not haveparts:
            part_type = random.choice(list(part_dir_dict.keys()))
            partlistdir = part_dir_dict[part_type] #directional
            partlistuni = part_uni_dict[part_type] #non-directional
            haveparts = len(partlistdir) != 0 or len(partlistuni) != 0
    partlistdir = part_dir_dict[part_type] #directional
    partlistuni = part_uni_dict[part_type] #non-directional
    if center:
        dir_chance = 0
    random.shuffle(partlistdir)
    random.shuffle(partlistuni)
    uniMode = False
    if random.random() <= dir_chance:
        if(len(partlistdir) != 0):
            part = pick_part_dir(partlistdir[0])
        else:
            part = Image.open(partlistuni[0]+".png")
            part = [part,
                    part]
            uniMode = True
    else:
        if(len(partlistuni) == 0):
            part = pick_part_dir(partlistdir[0])
        else:
            part = Image.open(partlistuni[0]+".png")
            part = [part,
                    part]
            uniMode = True
    #==============================================PART SCALING
    scale_rand = random.uniform(scaleRange[0],scaleRange[1])
    if part_type == "greeble":
        scale_rand = random.uniform(scaleRange[0]/5,scaleRange[1]/2)
    Rescale = True
    while Rescale:
        new_size = [round(part[0].size[0] * scale_rand), round(part[0].size[1] * scale_rand)]
        # part[Left/Right][Width,height]
        part = [p.resize(new_size) for p in part]
        part_size = [p.size for p in part]
        for n in range(len(part_size)):
            if part_size[n][0] > centW*1:
                scale_rand -= .1
            elif part_size[n][1] > centH*1:
                scale_rand -= .1
            else:
                Rescale = False
    #Coord base on center of image for X, top for Y sry for weird coordinate  
    #Basically it always gets mirrored on X, for Y I'm too lazy to mess with negatives.
    if clustermode:
        default_bound_min = [centW*(1-bound_minX),centH*(1-bound_minY)] #to leave some empty pixels on the edge, hopefully.    
        default_bount_max = [(centW*bound_constrainX),(height*bound_constrainY)]
    else:
        default_bound_min = [centW*(1-bound_minX),centH*(1-bound_minY)] #to leave some empty pixels on the edge, hopefully.    
        default_bount_max = [(centW*bound_constrainX),(height*bound_constrainY)]
    
    #area for the part to be placed.
    if boundmax == [0,0] and not clustermode:
        if part_type == 'gun':
            boundmin = [default_bound_min[0],part_size[0][1]+5]
            boundmax = [width*gun_max_W,(height*gun_max_H)+part_size[0][1]]
        elif part_type == 'engine':
            boundmin = [part_size[0][0],(centH*engine_min_H)-part_size[0][1]]
            boundmax = default_bount_max
        elif part_type == 'turret':
            boundmin = [p*.7 for p in default_bound_min]
            boundmax = [p*.7 for p in default_bount_max]
        elif part_type == 'greeble':
            boundmin = [default_bound_min[0]*0,(centH*engine_min_H)-part_size[0][1]]
            boundmax = [default_bount_max[0]/2,default_bount_max[1]*.7]
            straypercentX = .1
            straypercentY = .7
        else:
            boundmin = [0+part_size[0][0],0+part_size[0][1]]
            boundmax = default_bount_max
    
    loop = 0
    if len(bounddict.keys()) > 0:
        newboundmin = bounddict['min']
        newboundmax = bounddict['max']
    else:
        newboundmin = []
        newboundmax = []

    hardpoint = {}
    #trimodefuncX = -math.sqrt(boundmax[0])
    #trimodefuncY = (boundmin[1]+boundmax[1])/2
    gaussmode = True
    staticcount = count
    tocorner = 0
    c = 0
    b = 0
    if uniMode:
        partlistany = partlistuni
    else:
        partlistany = partlistdir
    if symmetric and not center and count > 1:
        
        #place in pairs
        i = 0
        while count > 1:
            #Randomized Pos
            #clustermode will place parts within area of previous part.
            if len(newboundmin) == 0 or not clustermode:
                rXmin = round(centW)
                #rXmin = max(centW,rXmin)
                if gaussmode:
                    rXmax = round(boundmax[0]+1-part_size[0][0]/2)
                    rXavg,rXdv = avg_deviation([rXmin,rXmax])
                    randX = round(random.gauss(rXmin,rXdv*10))
                    randX = min(randX,rXmax)
                    randX = max(randX,rXmin)
                    rYmin = round(boundmin[1])
                    rYmax = round(boundmax[1]+1-part_size[0][1]/2)
                    rYavg,rYdv = avg_deviation([rYmin,rYmax])
                    randY = round(random.gauss(rYmax/2,rYdv*5))
                    randY = min(randY,rYmax)
                    randY = max(randY,rYmin)
                else:
                    rXmax = round(boundmax[0]+1-part_size[0][0]/2)
                    randX = round(random.triangular(rXmin,rXmax,rXmin))
                    rYmin = round(boundmin[1])
                    rYmax = round(boundmax[1]+1-part_size[0][1]/2)
                    randY = round(random.randrange(rYmin,rYmax))
            else:
                
                #NOTE:y is overriding X, might cause problems.
                if inputdictonly: #dict from input
                    part,part_size,rXmin,rXmax = get_part_pos(partlistany,bounddict['min'],bounddict['max'],'x',part,part_size,uniMode,core_img=core_img)
                else: #dict updated with recently placed
                    part,part_size,rXmin,rXmax = get_part_pos(partlistany,newboundmin,newboundmax,'x',part,part_size,uniMode,core_img=core_img)
                rXmin = max(centW,rXmin)
                randX = round(random.triangular(rXmin,rXmax))
                
                mu = 0
                kappa = 4
                #randN = random.vonmisesvariate(mu,kappa)
                #randX = remap(randN,0,6,rXmin,rXmax)
                cc = min(4,round(((width*.7)/(part_size[0][0]/2))/(staticcount/2)))
                if cc != 0:
                    if tocorner % cc == 0:
                        randX = rXmax
                        c += 1 
                randX = min(randX,rXmax)
                randX = round(max(randX,rXmin))
                if inputdictonly:
                    part,part_size,rYmin,rYmax = get_part_pos(partlistany,bounddict['min'],bounddict['max'],'y',part,part_size,uniMode,core_img=core_img)
                else:
                    part,part_size,rYmin,rYmax = get_part_pos(partlistany,newboundmin,newboundmax,'y',part,part_size,uniMode,core_img=core_img)
                randY = round(random.triangular(rYmin,rYmax)) #.1 weight make more vertical
                cb = round(((height*1)/(part_size[0][1]/2))/(staticcount/4))
                #randN = random.vonmisesvariate(mu,kappa)
                #randY = remap(randN,0,6,rYmin,rYmax)
                if cb != 0:
                    if tocorner % cb == 0:
                        b += 1
                        if b % 2 == 0:
                            randY = rYmax
                        else:
                            randY = rYmin
                randY = min(randY,rYmax)
                randY = round(max(randY,rYmin))
                tocorner += 1
                #print(f"X:{rXmin,rXmax}")
                #print(f"Y:{rYmin,rYmax}")
            #print(f"Sel:{[randX,randY]}")
            #NOTE: Y is sometimes slightly less than it should for some reason.
            posX = randX - round(part_size[0][0]/2) #+ centW
            posY = randY - round(part_size[0][1]/2) #+ centH #note pre=off
            core_img.paste(part[1],(posX, posY),part[1])
            newboundmin.append([posX,posY])
            #print(f"Newmin:{[posX,posY]}")
            nposX = randX + round(part_size[0][0]/2) #+ centW
            nposY = randY + round(part_size[0][1]/2) #+ centH
            newboundmax.append([nposX,nposY])
            #print(f"Newmax:{[nposX,nposY]}")
            if part_type == 'n':
                print(f"{part_type}:{randX,randY}")
                print(f"{part_type}:{posX,posY}")
                print(f"{part_type}:{nposX,nposY}")
                debugpart = Image.open("imgparts/human/qs-perimeter-r"+".png")
                core_img.paste(debugpart,(posX, posY),debugpart)
                debugpart2 = Image.open("imgparts/human/qs-perimeter-rd"+".png")
                core_img.paste(debugpart2,(nposX, nposY),debugpart2)
            #symX = centW - round(part_size[1][0]/2) - randX
            symX = width- round(part_size[1][0]/2) - randX + 1#it was 1 px off for some reason.
            core_img.paste(part[0],(symX, posY),part[0])
            if part_type == 'gun' or part_type == 'turret' or part_type == 'engine':
                hardpoint[i] = [randX,posY]
                hardpoint[i+1] = [symX,posY]
            count -= 2
            i += 2
            #core_img.save(f'generatedsprites/stp{count}.png')

        #place single in the middle
        if count == 1:
            randX = 0
            if len(newboundmin) == 0 or not clustermode:
                rYmin = round(boundmin[1])
                rYmax = round(boundmax[1]+1)
                #randY = round(random.randrange(rYmin,rYmax))
                canvasmin = abs(part_size[0][1]/2)
                canvasmax = (core_img.size[0])-part_size[0][1]*.5
                rposmin = max(rYmin,canvasmin)
                rposmax = min(rYmax,canvasmax) 
            else:
                #partlistuni should've been shuffled already, so should still be random.
                part,part_size,rYmin,rYmax = get_part_pos(partlistuni,newboundmin,newboundmax,'y',part,part_size,uniMode=True,core_img=core_img)
                
            randY = round(random.randrange(round(rYmin),round(rYmax+1))) 
            posX = randX - round(part_size[0][0]/2) #+ centW
            posY = randY - round(part_size[0][1]/2)
            core_img.paste(part[0],(posX, posY),part[0])

            newboundmin.append([posX,posY])
            #print(f"Newmin:{[posX,posY]}")
            nposX = randX + round(part_size[0][0]/2) #+ centW
            nposY = randY + round(part_size[0][1]/2)
            newboundmax.append([nposX,nposY])

            #DEBUG
            if part_type == 'n':
                print(f"core:{randX,randY}")
                print(f"core:{posX,posY}")
                print(f"core:{nposX,nposY}")
                debugpart = Image.open("imgparts/human/qs-perimeter-r"+".png")
                core_img.paste(debugpart,(posX, posY),debugpart)
                debugpart = Image.open("imgparts/human/qs-perimeter-rd"+".png")
                core_img.paste(debugpart,(nposX, nposY),debugpart)
            
            #print(f"Newmax:{[nposX,nposY]}")
            if part_type == 'gun' or part_type == 'turret' or part_type == 'engine':
                hardpoint[staticcount-count] = [randX,posY]
            count -= 1
            #core_img.save(f'generatedsprites/stp{count}.png')
    #===========================CENTER MODE
    elif center:
        while count > 0:
            if pattern != None:
                randX = 0
                if len(newboundmin) == 0 or not clustermode:
                    randY = round(random.randrange(round(boundmin[1]),round(boundmax[1]+1)))
                else:
                    m = random.randrange(len(newboundmin))
                    randY = round(random.randrange(round(newboundmin[m][1]),round(min(boundmax[1],newboundmax[m][1]))))
                randX += pattern[loop][0]*part_size[0][0]
                randY += pattern[loop][1]*part_size[0][1]
            else:
                randX = 0
                if len(newboundmin) == 0 or not clustermode:
                    rYmin = round(boundmin[1]+part_size[0][1]/2)
                    rYmax = round(boundmax[1]+1-part_size[0][1]/2)
                    randY = round(random.randrange(rYmin,rYmax))
                else:
                    part,part_size,rYmin,rYmax = get_part_pos(partlistuni,newboundmin,newboundmax,'y',part,part_size,uniMode=True,core_img=core_img)
                    randY = round(random.randrange(rYmin,rYmax))
            posX = randX - round(part_size[0][0]/2)
            posY = randY - round(part_size[0][1]/2) #+ centH
            core_img.paste(part[0],(posX + centW, posY),part[0])
            #symX = centW - round(part_size[0]/2) - randX 
            newboundmin.append([posX,posY])
            #print(f"Newmin:{[posX,posY]}")
            nposX = randX + round(part_size[0][0]/2) + centW
            nposY = randY + round(part_size[0][1]/2)
            newboundmax.append([nposX,nposY])
            #print(f"Newmax:{[nposX,nposY]}")
            #symY = posY
            count -= 1
            loop += 1
    #===============================ASYMMETRIC MODE
    else:
        while count > 0:
            if len(newboundmin) == 0 or not clustermode:
                randX = round(random.triangular(round(boundmin[0]),round(boundmax[0]+1),weightXAsym))
                randY = round(random.randrange(round(boundmin[1]),round(boundmax[1]+1)))
            else:
                if uniMode:
                    partlistany = partlistuni
                else:
                    partlistany = partlistdir
                part,part_size,rXmin,rXmax = get_part_pos(partlistany,newboundmin,newboundmax,'x',part,part_size,uniMode,core_img=core_img)
                randX = round(random.triangular(rXmin,rXmax, .1))
                part,part_size,rYmin,rYmax = get_part_pos(partlistany,newboundmin,newboundmax,'y',part,part_size,uniMode,core_img=core_img)
                randY = round(random.triangular(rYmin,rYmax, .1))
            posX = randX #- round(part_size[0][0]/2) + round(centW*.7)
            posY = randY #- round(part_size[0][1]/2) #+ centH
            side_sel = 1
            if centW-posX > 0:
                side_sel = 0
            core_img.paste(part[side_sel],(posX, posY),part[0])
            newboundmin.append([posX,posY])
            #print(f"Newmin:{[posX,posY]}")
            nposX = randX + round(part_size[0][0]/2)
            nposY = randY + round(part_size[0][1]/2)
            newboundmax.append([nposX,nposY])
            #print(f"Newmax:{[nposX,nposY]}")

            count -= 1
    bounddict = {}
    bounddict['min'] = newboundmin.copy()
    bounddict['max'] = newboundmax.copy()
    return core_img,bounddict,hardpoint

def generate_sprite(faction,category="Heavy Warship",width=0,height=0,part_list=[],gun=0,turret=0):
    
    #TODO consider ship data
    if category == "Drone" or category == "Fighter":
        width = random.randrange(80,100,2)
        height = random.randrange(80,100,2)
    elif category == "Interceptor":
        width = random.randrange(100,120,2)
        height = random.randrange(100,120,2)
    elif category == "Light Warship" or category == "Light Freighter":
        width = random.randrange(120,200,2)
        height = random.randrange(120,200,2)
    elif category == "Medium Warship":
        width = random.randrange(170,260,2)
        height = random.randrange(170,260,2)
    elif category == "Heavy Warship" or category == "Heavy Freighter":
        width = random.randrange(200,420,2)
        height = random.randrange(260,420,2)
    elif category == "Transport":
        width = random.randrange(120,260,2)
        height = random.randrange(120,260,2)

    print(f"Generating ship {category} with size {width,height}")
    part_dir_dict = part_list[0]
    part_uni_dict = part_list[1]
    centW = round(width/2)
    centH = round(height/2)
    gpoints = {}
    tpoints = {}

    pcs = (width*height)/(260*260) #ratio of pieces to place to HWdefault

    new_img = Image.new('RGBA', (width,height))

    #patternformat = [[OriginXY],[TranslationXY],...] in sprite size ratio. TODO: Turn into a function.
    #pattern_Hline = [[0,0],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1]]
    # 
    stacktype = 2
    if stacktype == 1: #Decent without clustermode.
        new_img,bounddict = place_parts(new_img,part_list,count=4,part_type='engine')
        new_img,bounddict = place_parts(new_img,part_list,count=1,part_type='core',bounddict=bounddict)
        new_img,bounddict = place_parts(new_img,part_list,count=4,part_type='gun',bounddict=bounddict)
        new_img,bounddict = place_parts(new_img,part_list,count=8,part_type='perimeter',bounddict=bounddict)
        new_img,bounddict = place_parts(new_img,part_list,count=32,part_type='body',bounddict=bounddict)
        new_img,bounddict = place_parts(new_img,part_list,count=16,part_type='body',bounddict=bounddict)
        new_img,bounddict = place_parts(new_img,part_list,count=8,part_type='body',bounddict=bounddict)
        new_img,bounddict = place_parts(new_img,part_list,count=16,part_type='greeble',bounddict=bounddict)
        new_img,bounddict = place_parts(new_img,part_list,count=16,part_type='greeble',bounddict=bounddict)
        new_img,bounddict = place_parts(new_img,part_list,count=1,part_type='turret',bounddict=bounddict)
        new_img,bounddict = place_parts(new_img,part_list,count=6,part_type='turret',bounddict=bounddict)
        new_img,bounddict = place_parts(new_img,part_list,count=1,part_type="cockpit",bounddict=bounddict)
    elif stacktype == 2:
        new_img,bounddictc,a = place_parts(new_img,part_list,count=1,part_type='core',boundmin=[0,centH],boundmax=[0,centH])
        #new_img,bounddictc = place_parts(new_img,part_list,count=4,part_type='body',bounddict=bounddictc)
        new_img,bounddictb,a = place_parts(new_img,part_list,count=64*pcs,part_type='body',bounddict=bounddictc,
                                                                                    clustermode=True)
        new_img,bounddict,a = place_parts(new_img,part_list,count=8*pcs,part_type='body',bounddict=bounddictc,
                                                                                    clustermode=True)
        new_img,bdg,gpoints = place_parts(new_img,part_list,count=gun,part_type='gun',bounddict=bounddictb,
                                                                                    clustermode=True)
        new_img,bounddict,a = place_parts(new_img,part_list,count=8*pcs,part_type='perimeter',bounddict=bounddictb,
                                                                                    clustermode=True)
        new_img,bounddict,a = place_parts(new_img,part_list,count=8*pcs,part_type='body',bounddict=bounddictb,
                                                                                    clustermode=True)
        new_img,bounddict,a = place_parts(new_img,part_list,count=0,part_type='greeble',bounddict=bounddictb,
                                                                                    clustermode=True)
        new_img,bounddict,tpoints = place_parts(new_img,part_list,count=turret,part_type='turret',bounddict=bounddictb,
                                                                                    clustermode=True)
        new_img,bounddict,a = place_parts(new_img,part_list,count=1,part_type='cockpit',bounddict=bounddict,
                                                                                    clustermode=True)
    elif stacktype == 3: #pug
        new_img,bounddictc = place_parts(new_img,part_list,count=1,part_type='core',boundmin=[0,centH],boundmax=[0,centH])
        new_img,bounddictc = place_parts(new_img,part_list,count=6,part_type='body',bounddict=bounddictc)
        new_img,bounddictb = place_parts(new_img,part_list,count=2,part_type='body',bounddict=bounddictc,
                                                                                    clustermode=True,inputdictonly = True)
        new_img,bounddict = place_parts(new_img,part_list,count=3,part_type='body',bounddict=bounddictc,
                                                                                    clustermode=True)
        new_img,bounddict = place_parts(new_img,part_list,count=16,part_type='perimeter',bounddict=bounddictb,
                                                                                    clustermode=True)
        new_img,bounddictg = place_parts(new_img,part_list,count=4,part_type='gun',bounddict=bounddictb,
                                                                                    clustermode=True)
        new_img,bounddict = place_parts(new_img,part_list,count=16,part_type='perimeter',bounddict=bounddictb,
                                                                                    clustermode=True)
        new_img,bounddict = place_parts(new_img,part_list,count=8,part_type='body',bounddict=bounddictb,
                                                                                    clustermode=True)
        new_img,bounddict = place_parts(new_img,part_list,count=0,part_type='greeble',bounddict=bounddictb,
                                                                                    clustermode=True)
        new_img,bounddict = place_parts(new_img,part_list,count=8,part_type='turret',bounddict=bounddictb,
                                                                                    clustermode=True)
        new_img,bounddict = place_parts(new_img,part_list,count=1,part_type='cockpit',bounddict=bounddict,
                                                                                    clustermode=True)
    elif stacktype == 99:
        new_img,bounddictc = place_parts(new_img,part_list,count=1,part_type='core')
        new_img,bounddictb = place_parts(new_img,part_list,count=2,part_type='body',bounddict=bounddictc,
                                                                                    clustermode=True)
    
    gradient = Image.linear_gradient('L')
    gradient = gradient.rotate(90)
    gradient = gradient.resize((width,height), resample=Image.BICUBIC)
    gradient = gradient.convert('RGBA')
    gradient.paste(new_img,(0,0),gradient)

    new_img = Image.blend(new_img,gradient,.5)

    #Make sure there's an empty pixel around the image.
    boarderimg = Image.new('RGBA', (width+2,height+2))
    boarderimg.paste(new_img,(1, 1),new_img)

    return boarderimg,gpoints,tpoints
    #new_img.save('test.png')
    #new_img.show()
StandaloneMode = False
TestMode = False
if StandaloneMode:
    part_sel = input("Choose part type(default:human): ")
    if part_sel == "":
        part_sel = "human"
    cat = input("Choose category(default:Heavy Warship): ")
    if cat == "":
        cat = "Heavy Warship"
    try:
        num = int(input("Number to generate(default:5): "))
    except ValueError:
        num = 5
elif TestMode:
    part_sel = "human"
    cat = "Interceptor"
    num = 100
    #part_list=get_sprites(setselect="human") 
    part_list=get_sprites(setselect=part_sel) 
    for n in range(num):
        sprite,gpoints,tpoints = generate_sprite(None,category=cat,part_list=part_list)
        try:
            sprite.save(f'generatedsprites/{n}.png')
        except FileNotFoundError:
            os.makedirs('generatedsprites')

def call_generate_sprite(faction,category,name,gun,turret):
    gunlistx = []
    gunlisty = []
    turlistx = []
    turlisty = []
    part_list=get_sprites(setselect=faction.partset) 
    sprite,gpoints,tpoints = generate_sprite(faction,category,gun=gun,turret=turret,part_list=part_list)
    try:
        os.makedirs(f'images/ship/{faction.name}')
    except FileExistsError:
        pass
    sprite.save(f'images/ship/{faction.name}/{name}.png')
    for i,gunxy in gpoints.items():
        gunlistx.append(gunxy[0])
        gunlisty.append(gunxy[1])
    for i,turxy in tpoints.items():
        turlistx.append(turxy[0])
        turlisty.append(turxy[1])

    return gunlistx,gunlisty,turlistx,turlisty