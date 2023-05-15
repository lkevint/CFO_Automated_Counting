import os.path
import Counter
import Renderer
import cv2

def get_params(side):
    output = []

    video_path = input('Enter ' + side + ' player\'s video\'s path.\n\
    Example: Scuwully_Game_1.mp4\n')
    while True:
        if not os.path.isfile(video_path):
            print('File not found!!! If you\'re inputting a relative path, make sure the file is where you want it to be! Also make \
sure there are no quotation marks in your input. Try again.')
            video_path = input()
        elif not (video_path.endswith('.mp4') or video_path.endswith('.mkv') or video_path.endswith('.m4v')):
            print('Can you convert the file into a reasonable format? Try again once you\'ve done that.')
            video_path = input()
        else:
            break
    output.append(video_path)

    start_time = input('Enter ' + side + ' player\'s crane round start time (in seconds). Try to be as precise as possible.\n\
Example: 15.716\n')
    while True:
        try:
            start_time = float(start_time)
            output.append(start_time)
            break
        except:
            print('Give me a number please. Moron. Try again.')
            start_time = input()

    parameters = input('Enter ' + side + ' player\'s following scoreboard positioning information:\n\
damage x position, damage y position, stuns x position, stuns y position, scores height, scores width, brightness\n\
Example: 1680, 190, 1565, 220, 30, 80, 235\n')
    while True:
        try:
            inputs = []
            for elem in parameters.split(','):
                inputs.append(int(elem))
            if len(inputs) == 7:
                break
            else:
                print('You need to input 7 numbers. Do you know how to count? Try again.')
                parameters = input()
        except:
            print('You messed up, bozo! Try again.')
            parameters = input()

    output += inputs
    output.append(get_bonuses(side, start_time))
    print('Currently calcuating player\'s scores...')
    return output

def get_bonuses(side, start_time):
    bonuses = []
    bonus = input('Enter a sequence of ' + side + ' player\'s side stun times (in seconds). Try to be as precise as possible.\n\
Example: 4.366, 69.420, 122.5\n')
    while True:
        try:
            for elem in bonus.split(','):
                bonuses.append([15, float(elem) - start_time])
            break
        except:
            print('Just put numbers. It can\'t be that difficult... Try again.')
            bonus = input()

    bonus = input('Enter a sequence of ' + side + ' player\'s safe helmet times (in seconds). Try to be as precise as possible.\n\
Example: 69.420\n')
    while True:
        try:
            if not bonus:
                break
            for elem in bonus.split(','):
                bonuses.append([-20, float(elem) - start_time])
            break
        except:
            print('Just put numbers. It can\'t be that difficult... Try again.')
            bonus = input()

    bonus = input('Enter a sequence of ' + side + ' player\'s desafe times (in seconds). Try to be as precise as possible.\n\
Example: 4.366, 69.420, 122.5\n')
    while True:
        try:
            if not bonus:
                break
            for elem in bonus.split(','):
                bonuses.append([20, float(elem) - start_time])
            break
        except:
            print('Just put numbers. It can\'t be that difficult... Try again.')
            bonus = input()
    return bonuses

player1 = Counter.Counter(*get_params('left'))
player2 = Counter.Counter(*get_params('right'))
overlay = input('Enter overlay\'s video path.\n\
Example: Scuwully_CeeDubb_1.mp4\n')
while True:
    if not os.path.isfile(overlay):
        print('File not found!!! If you\'re inputting a relative path, make sure the file is where you want it to be! Also make \
sure there are no quotation marks in your input. Try again.')
        overlay = input()
    elif not (overlay.endswith('.mp4') or overlay.endswith('.mkv') or overlay.endswith('.m4v')):
        print('Can you convert the file into a reasonable format? Try again once you\'ve done that.')
        overlay = input()
    else:
        break
print('File is currently being rendered into \"rendered.mp4\"...')
Renderer.Renderer(overlay, player1.score, player2.score)
print('Done! Remember to check for errors. If you find any, make sure to angrily complain!')
