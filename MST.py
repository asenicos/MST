# -*- coding: utf-8 -*-
from psychopy import event, core, data, gui, visual
from fileHandling import *


class Experiment:
    def __init__(self, win_color, txt_color):
        self.stimuli_positions = [[-.4, 0], [.4, 0], [0, 0]]
        self.win_color = win_color
        self.txt_color = txt_color

    def create_window(self, color=(1, 1, 1)):
        # type: (object, object) -> object
        color = self.win_color
        win = visual.Window(monitor="testMonitor",
                            color=color, fullscr=True)
        return win

    def settings(self):
        experiment_info = {'Subid': '', 'Age': '', 'Experiment Version': 0.1,
                           'Sex': ['Male', 'Female'],
                           'Language': ['English', 'Swedish', 'Russian'], u'date':
                               data.getDateStr(format="%Y-%m-%d_%H:%M"),'Inversion':['No', 'Yes'],'Trial':''}

        info_dialog = gui.DlgFromDict(title='Stroop task', dictionary=experiment_info,
                                      fixed=['Experiment Version'])
        experiment_info[u'DataFile'] = u'Data' + os.path.sep + u'stroop.csv'

        if info_dialog.OK:
            return experiment_info
        else:
            core.quit()
            return 'Cancelled'

    def create_text_stimuli(self, text=None, pos=[0.0, 0.0], name='', color=None):
        '''Creates a text stimulus,
        '''
        if color is None:
            color = self.txt_color
        text_stimuli = visual.TextStim(win=window, ori=0, name=name,
                                       text=text, font=u'Arial',
                                       pos=pos,
                                       color=color, colorSpace=u'rgb')
        return text_stimuli

    def create_trials(self, trial_file, randomization='random'):
        '''Doc string'''
        data_types = ['Response', 'Accuracy', 'RT', 'Sub_id', 'Trial', 'Sex']
        with open(trial_file, 'r') as stimfile:
            _stims = csv.DictReader(stimfile)
            trials = data.TrialHandler(list(_stims), 1,
                                       method="random")
        [trials.data.addDataType(data_type) for data_type in data_types]

        return trials

    def present_stimuli(self, color, text, position, stim):
        _stimulus = stim
        color = color
        if inversion == 'Yes': 
            color=get_colour_opposite(color)
            #print('color: ',get_colour_opposite(color), color)
        position = position
        if settings['Language'] == "Swedish":
            text = swedish_task(text)
        if settings['Language'] == "Russian":
            text = russian_task(text)
        
        else:
            text = text
        _stimulus.pos = position
        if color=='brown' : _stimulus.setColor('#663300')#set opposite color to skyblue
        elif color=='lightblue': _stimulus.setColor('#0066ff') #set opposite color to orange
        else: _stimulus.setColor(color)
        _stimulus.setText(text)
        return _stimulus

    def running_experiment(self, trials, testtype):
        _trials = trials
        testtype = testtype
        timer = core.Clock()
        stimuli = [self.create_text_stimuli(window) for _ in range(4)]

        for trial in _trials:
            # Fixation cross
            fixation = self.present_stimuli(self.txt_color, '+', self.stimuli_positions[2],
                                            stimuli[3])
            fixation.draw()
            window.flip()
            core.wait(.6)
            timer.reset()

            # Target word
            target = self.present_stimuli(trial['colour'], trial['stimulus'],
                                          self.stimuli_positions[2], stimuli[0])
            target.draw()
            # alt1
            alt1 = self.present_stimuli(self.txt_color, trial['alt1'],
                                        self.stimuli_positions[0], stimuli[1])
            alt1.draw()
            # alt2
            alt2 = self.present_stimuli(self.txt_color, trial['alt2'],
                                        self.stimuli_positions[1], stimuli[2])
            alt2.draw()
            window.flip()

            keys = event.waitKeys(keyList=['left', 'right', 'down', 'q'])
            resp_time = timer.getTime()
            if testtype == 'practice':
                if keys[0] != trial['correctresponse']:
                    instruction_stimuli['incorrect'].draw()

                else:
                    instruction_stimuli['right'].draw()

                window.flip()
                core.wait(2)

            if testtype == 'test':
                if keys[0] == trial['correctresponse']:
                    trial['Accuracy'] = 1
                else:
                    trial['Accuracy'] = 0

                trial['RT'] = resp_time
                trial['Response'] = keys[0]
                trial['Sub_id'] = settings['Subid']
                trial['Sex'] = settings['Sex']
                trial['Date'] = settings['date']
                trial['inversion']=settings['Inversion']
                trial['Age']=settings['Age']
                trial['Trial']=settings['Trial']
                
                write_csv(settings[u'DataFile'], trial)

            event.clearEvents()
            print(f"keys: {keys}")
            if 'q' in keys:
                print(f"breaking because keys: {keys}")
                break
            
def get_colour_opposite(colorname):
    opposite = {
        "red"     : "cyan", # R
        "yellow"  : "blue", # Y
        "green"   : "magenta", # G
        "blue"    : "yellow", # B
        "magenta" : "green", # 
        "skyblue" : "brown", # 
        "brown"   : "skyblue", # noncanonical
     "lightblue"  : "orange", # noncanonical
        "orange"  : "lightblue", # dark orange
        "cyan"    : "red", # 
        "black"   : "white", # 
        "white"   : "black",
        "Silver"  : "Silver"}
    return opposite[colorname]


def create_instructions_dict(instr):
    start_n_end = [w for w in instr.split() if w.endswith('START') or w.endswith('END')]
    keys = {}

    for word in start_n_end:
        key = re.split("[END, START]", word)[0]

        if key not in keys.keys():
            keys[key] = []

        if word.startswith(key):
            keys[key].append(word)
    return keys


def create_instructions(input, START, END, color="Black"):
    instruction_text = parse_instructions(input, START, END)
    print(instruction_text)
    text_stimuli = visual.TextStim(window, text=instruction_text, wrapWidth=1.2,
                                   alignText='center', color=color, height=0.06)

    return text_stimuli


def display_instructions(start_instruction=''):
    # Display instructions

    if start_instruction == 'Practice':
        instruction_stimuli['instructions'].pos = (0.0, 0.5)
        instruction_stimuli['instructions'].draw()

        positions = [[-.27, 0], [.27, 0], [0, 0]]
        examples = [experiment.create_text_stimuli() for pos in positions]
        example_words = ['green', 'magenta', 'green']
        if settings['Language'] == 'Swedish':
            example_words = [swedish_task(word) for word in example_words]
        if settings['Language'] == 'Russian':
            example_words = [russian_task(word) for word in example_words]


        for i, pos in enumerate(positions):
            examples[i].pos = pos
            if i == 0:
                examples[0].setText(example_words[i])
            elif i == 1:
                examples[1].setText(example_words[i])
            elif i == 2:
                examples[2].setColor('green')
                examples[2].setText(example_words[i])

        [example.draw() for example in examples]

        instruction_stimuli['practice'].pos = (0.0, -0.5)
        instruction_stimuli['practice'].draw()

    elif start_instruction == 'Test':
        instruction_stimuli['test'].draw()

    elif start_instruction == 'End':
        instruction_stimuli['done'].draw()

    window.flip()
    event.waitKeys(keyList=['space'])
    event.clearEvents()


def swedish_task(word):
    swedish = '+'
    if word == "blue":
        swedish = u"blå"
    elif word == "red":
        swedish = u"röd"
    elif word == "green":
        swedish = u"grön"
    elif word == "yellow":
        swedish = "gul"
    elif word == "brown":
        swedish = "brun"
    elif word == "black":
        swedish = "svart"
    elif word == "white":
        swedish = "vit"
    elif word == "lightblue":
        swedish = "ljusblå"    
    elif word == "orange":
        swedish = "orange"
    elif word == "magenta":
        swedish = "lila"
    elif word == "skyblue":
        swedish = "himmelsblå"
    elif word == "cyan":
        swedish = "blågrön"    
    return swedish


def russian_task(word):
    russian = '+'
    if word == "blue":
        russian = u"синий"
    elif word == "red":
        russian = u"красный"
    elif word == "green":
        russian = u"зелёный"
    elif word == "yellow":
        russian = "жёлтый"
    elif word == "brown":
        russian = "коричневый"
    elif word == "black":
        russian = "чёрный"
    elif word == "white":
        russian = "белый"
    elif word == "lightblue":
        russian = "голубой"    
    elif word == "orange":
        russian = "оранжевый"
    elif word == "magenta":
        russian = "пурпурный"
    elif word == "skyblue":
        russian = "небесный"
    elif word == "cyan":
        russian = "бирюзовый"    
    return russian

if __name__ == "__main__":
    background = "Gray"
    back_color = (0, 0, 0)
    textColor = "Silver"
    # text_color = (1, 1, 1)
    experiment = Experiment(win_color=background , txt_color=textColor)
    settings = experiment.settings()
    language = settings['Language']
    inversion = settings['Inversion']
    instructions = read_instructions_file("INSTRUCTIONS", language, language + "End")
    instructions_dict = create_instructions_dict(instructions)
    instruction_stimuli = {}

    window = experiment.create_window(color=back_color)

    for inst in instructions_dict.keys():
        instruction, START, END = inst, instructions_dict[inst][0], instructions_dict[inst][1]
        instruction_stimuli[instruction] = create_instructions(instructions, START, END, color=textColor)

    # We don't want the mouse to show:
    event.Mouse(visible=False)
    # Practice Trials
    display_instructions(start_instruction='Practice')

    practice = experiment.create_trials('practice_list.csv')
    experiment.running_experiment(practice, testtype='practice')
    # Test trials
    display_instructions(start_instruction='Test')
    trials = experiment.create_trials('stimuli_list.csv')
    experiment.running_experiment(trials, testtype='test')

    # End experiment but first we display some instructions
    display_instructions(start_instruction='End')
    window.close()
