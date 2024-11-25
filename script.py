import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )
    knobs = []
    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'
    frames = 0
    basename = ""
    aniLoop = 0
    finalFrame = 0
    
    if aniLoop == 0:
        for command in commands:
            c = command['op']
            args = command['args']
            if c == 'frames':
                frames = args[0]
                finalFrame = frames
            if c == 'basename':
                basename = args[0]
            if c == 'vary' and frames == 0:
                print("frames have not been set")
                break
            if frames != 0 and basename == '':
                print('frames have been set, but not base name')
                print('setting basename to default00')
                basename = 'default00'
        aniLoop += 1

    if aniLoop == 1:
        for command in commands:  
            c = command['op']
            args = command['args']  
            if c == 'vary':
                currentFrame = args[0]
                finalFrame = args[1]
                change = 1/frames
                while currentFrame <= finalFrame:
                    d = args[3]-args[2]
                    knobName = command['knob']
                    knobs.append({knobName:change*currentFrame})
                    currentFrame += 1
        aniLoop += 1
        print(knobs)
                
        
    if aniLoop == 2 and frames > 1:
        aniLoop += 1
        currentFrame = 1
        while currentFrame <= finalFrame:
            for command in commands:
                print(command)
                c = command['op']
                args = command['args']
                if c == 'vary' and currentFrame >= args[0] and currentFrame <= args[1]:
                    symbols[command['knob']] = knobs[currentFrame][command['knob']]
                    print(symbols[command['knob']])
                elif c == 'vary':
                    symbols[command['knob']] = 0
                if c == 'box':
                    if command['constants']:
                        reflect = command['constants']
                    add_box(tmp,
                            args[0], args[1], args[2],
                            args[3], args[4], args[5])
                    matrix_mult( stack[-1], tmp )
                    draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                    tmp = []
                    reflect = '.white'
                elif c == 'sphere':
                    if command['constants']:
                        reflect = command['constants']
                    add_sphere(tmp,
                            args[0], args[1], args[2], args[3], step_3d)
                    matrix_mult( stack[-1], tmp )
                    draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                    tmp = []
                    reflect = '.white'
                elif c == 'torus':
                    if command['constants']:
                        reflect = command['constants']
                    add_torus(tmp,
                            args[0], args[1], args[2], args[3], args[4], step_3d)
                    matrix_mult( stack[-1], tmp )
                    draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                    tmp = []
                    reflect = '.white'
                elif c == 'line':
                    add_edge(tmp,
                            args[0], args[1], args[2], args[3], args[4], args[5])
                    matrix_mult( stack[-1], tmp )
                    draw_lines(tmp, screen, zbuffer, color)
                    tmp = []
                elif c == 'move':
                    if(command['knob'] != None):
                        tmp = make_translate(args[0] * symbols[command['knob']], args[1] * symbols[command['knob']], args[2] * symbols[command['knob']])
                        matrix_mult(stack[-1], tmp)
                        stack[-1] = [x[:] for x in tmp]
                        tmp = []
                    else:
                        tmp = make_translate(args[0], args[1], args[2])
                        matrix_mult(stack[-1], tmp)
                        stack[-1] = [x[:] for x in tmp]
                        tmp = []
                elif c == 'scale':
                    if(command['knob'] != None):
                        tmp = make_scale(args[0] * symbols[command['knob']], args[1] * symbols[command['knob']], args[2] * symbols[command['knob']])
                        matrix_mult(stack[-1], tmp)
                        stack[-1] = [x[:] for x in tmp]
                        tmp = []
                    else:
                        tmp = make_scale(args[0], args[1], args[2])
                        matrix_mult(stack[-1], tmp)
                        stack[-1] = [x[:] for x in tmp]
                        tmp = []
                elif c == 'rotate':
                    if(command['knob'] != None):
                        theta = args[1] * (math.pi/180)
                        if args[0] == 'x':
                            tmp = make_rotX(theta* symbols[command['knob']])
                        elif args[0] == 'y':
                            tmp = make_rotY(theta* symbols[command['knob']])
                        else:
                            tmp = make_rotZ(theta* symbols[command['knob']])
                        matrix_mult( stack[-1], tmp )
                        stack[-1] = [ x[:] for x in tmp]
                        tmp = []
                    else:    
                        theta = args[1] * (math.pi/180)
                        if args[0] == 'x':
                            tmp = make_rotX(theta)
                        elif args[0] == 'y':
                            tmp = make_rotY(theta)
                        else:
                            tmp = make_rotZ(theta)
                        matrix_mult( stack[-1], tmp )
                        stack[-1] = [ x[:] for x in tmp]
                        tmp = []
                elif c == 'push':
                    stack.append([x[:] for x in stack[-1]] )
                elif c == 'pop':
                    stack.pop()
                elif c == 'save':
                    save_extension(screen, args[0] + "0" + str(currentFrame) + ".png")
            clear_screen(screen)
            clear_zbuffer(zbuffer)
            currentFrame += 1


    if aniLoop != 2:
        for command in commands:
            print(command)
            c = command['op']
            args = command['args']

            if c == 'box':
                if command['constants']:
                    reflect = command['constants']
                add_box(tmp,
                        args[0], args[1], args[2],
                        args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'sphere':
                if command['constants']:
                    reflect = command['constants']
                add_sphere(tmp,
                        args[0], args[1], args[2], args[3], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'torus':
                if command['constants']:
                    reflect = command['constants']
                add_torus(tmp,
                        args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'line':
                add_edge(tmp,
                        args[0], args[1], args[2], args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_lines(tmp, screen, zbuffer, color)
                tmp = []
            elif c == 'move':
                if(command['knob'] != None):
                    tmp = make_translate(args[0] * symbols[command['knob']], args[1] * symbols[command['knob']], args[2] * symbols[command['knob']])
                    matrix_mult(stack[-1], tmp)
                    stack[-1] = [x[:] for x in tmp]
                    tmp = []
                else:
                    tmp = make_translate(args[0], args[1], args[2])
                    matrix_mult(stack[-1], tmp)
                    stack[-1] = [x[:] for x in tmp]
                    tmp = []
            elif c == 'scale':
                if(command['knob'] != None):
                    tmp = make_scale(args[0] * symbols[command['knob']], args[1] * symbols[command['knob']], args[2] * symbols[command['knob']])
                    matrix_mult(stack[-1], tmp)
                    stack[-1] = [x[:] for x in tmp]
                    tmp = []
                else:
                    tmp = make_scale(args[0], args[1], args[2])
                    matrix_mult(stack[-1], tmp)
                    stack[-1] = [x[:] for x in tmp]
                    tmp = []
            elif c == 'rotate':
                if(command['knob'] != None):
                    theta = args[1] * (math.pi/180)
                    if args[0] == 'x':
                        tmp = make_rotX(theta* symbols[command['knob']])
                    elif args[0] == 'y':
                        tmp = make_rotY(theta* symbols[command['knob']])
                    else:
                        tmp = make_rotZ(theta* symbols[command['knob']])
                    matrix_mult( stack[-1], tmp )
                    stack[-1] = [ x[:] for x in tmp]
                    tmp = []
                else:    
                    theta = args[1] * (math.pi/180)
                    if args[0] == 'x':
                        tmp = make_rotX(theta)
                    elif args[0] == 'y':
                        tmp = make_rotY(theta)
                    else:
                        tmp = make_rotZ(theta)
                    matrix_mult( stack[-1], tmp )
                    stack[-1] = [ x[:] for x in tmp]
                    tmp = []
            elif c == 'push':
                stack.append([x[:] for x in stack[-1]] )
            elif c == 'pop':
                stack.pop()
            elif c == 'display':
                display(screen)
            elif c == 'save':
                save_extension(screen, args[0])
