from constants import *
import camera
import levels
from pyglet.gl import *

window = pyglet.window.Window(caption = "Vzostup Amaz'hán",
                              width = width,
                              height = height)

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
window.set_mouse_visible(True)
pyglet.font.add_file('Cardinal.ttf')
action_man = pyglet.font.load('Cardinal')
speaker = pyglet.media.Player()
effects = pyglet.media.Player()
effects.queue(explosion)
looper = pyglet.media.SourceGroup(explosion.audio_format, None)
looper.loop = True
looper.queue(audio_levels["MENU"])
speaker.queue(looper)
speaker.play()

last = 0

with open("last", "r") as fi:
    last = int(fi.read())
    
print(last)


class GameState:
    def __init__(self):
        self.current_level = last + 1
        self.max_level = 8
        self.exploded = False
        self.level = levels.Level(self.current_level)
        
    def draw(self):
        self.level.draw()
    
    def update(self, dt):
        return "GAME"
    
    def next_level(self):
        self.current_level += 1
        if self.current_level > self.max_level:
            quit()
        self.level = levels.Level(self.current_level)
        self.exploded = False
        
    def key_press(self, key):
        if not key in pressed or key == pyglet.window.key.ESCAPE:
            loop = pyglet.media.SourceGroup(audio_levels["MENU"].audio_format, None)
            loop.loop = True
            loop.queue(audio_levels["MENU"])
            speaker.queue(loop)
            speaker.next_source()
            return "MENU"
        res = self.level.step(key)
        print("res {}, key je {}".format(res, key))
        if res != None:
            print("Tvoj vysledok je {}".format(res))
            self.exploded = True
            effects.queue(explosion)
            effects.play()
            states["WIN"].set_score(res)
            loop = pyglet.media.SourceGroup(audio_levels["WIN"].audio_format, None)
            loop.loop = True
            loop.queue(audio_levels["WIN"])
            speaker.queue(loop)
            speaker.next_source()
            return "WIN"
        return "GAME"
    
    def replay_level(self):
        self.level = levels.Level(self.current_level)
        
    def new_game(self):
        print("NOVO HRA? ")
        self.current_level = 1
        self.level = levels.Level(self.current_level)

class WinState:
    def __init__(self):
        amazhana = pyglet.resource.image(os.path.join("graphics", "Dead1.png"))
        self.amazsprite = pyglet.sprite.Sprite(amazhana, x = width / 3, y = height / 3)
        self.amazsprite.scale = 3
        #self.amazsprite.rotation = 
        star_full = pyglet.resource.image(os.path.join("graphics", "full.png"))
        star_full.width = 200
        star_full.height = 200
        star_blank = pyglet.resource.image(os.path.join("graphics", "blank.png"))
        star_blank.width = 200
        star_blank.height = 200
        self.stars = [pyglet.sprite.Sprite(pyglet.resource.image(os.path.join("graphics", str(i) + ".png")), x = width / 2 - 250, y = height / 2) for i in range(4)]
        for star in self.stars:
            star.scale = 7
        self.score = 0
        self.res = 0
        self.text = pyglet.text.Label("Press key to continue" , font_name = 'Cardinal', font_size = 60, anchor_x = 'center', anchor_y = 'center', x = width // 2, y = height / 2 - 200, color = (255, 0, 0, 255))
        
    def set_score(self, score):
        self.score, self.res = score
        
    def update(self, dt):
        return "WIN"
    
    def key_press(self, key):
        states["TALE"].set_level_score(states["GAME"].current_level, self.score)
        loop = pyglet.media.SourceGroup(audio_levels["TALE"].audio_format, None)
        loop.loop = True
        loop.queue(audio_levels["TALE"])
        speaker.queue(loop)
        speaker.next_source()
        return "TALE"
    
    def draw(self):
        states["GAME"].draw()
        self.amazsprite.draw()
        self.stars[self.score].draw()
        self.text.draw()

class MenuState:
    def __init__(self):
        global states
        self.bars = [pyglet.sprite.Sprite(pyglet.resource.image(os.path.join("graphics", "menu.png")), x = width // 2 - 300, y = height - 300 - i * 200) for i in range(4)]
        for bar in self.bars:
            bar.scale = 0.25
        self.pointer = pyglet.sprite.Sprite(pyglet.resource.image(os.path.join("graphics", "choose.png")), x = width // 2 - 300, y = height - 300)
        self.pointer.scale = 0.25
        self.kde = 0
        self.texts = [pyglet.text.Label("End Game", font_name = 'Cardinal', font_size = 40, anchor_x = 'center', anchor_y = 'center', x = width // 2 + 30, y = height - 770),
                      pyglet.text.Label("Replay Level", font_name = 'Cardinal', font_size = 40, anchor_x = 'center', anchor_y = 'center', x = width // 2 + 30, y = height - 570),
                      pyglet.text.Label("Resume Game", font_name = 'Cardinal', font_size = 40, anchor_x = 'center', anchor_y = 'center', x = width // 2 + 30, y = height - 370),
                      pyglet.text.Label("New Game", font_name = 'Cardinal', font_size = 40, anchor_x = 'center', anchor_y = 'center', x = width // 2 + 30, y = height - 170)]
        self.actions = [self.save, self.replay_level, self.resume, self.new_game]
        self.actions = list(reversed(self.actions))
        
    def update(self, dt):
        return "MENU"
    
    def key_press(self, key):
        if key in pressed and key != pyglet.window.key.ENTER:
            if key == pyglet.window.key.W:
                self.kde -= 1
            if key == pyglet.window.key.S:
                self.kde += 1
            self.kde = (self.kde + 4) % 4
            self.pointer.set_position(self.pointer.x, height - 300 - self.kde * 200)
            return "MENU"
        else:
            print(self.kde)
            return self.actions[self.kde]()
    
    def draw(self):
        for bar in self.bars:
            bar.draw()
        self.pointer.draw()
        for text in self.texts:
            text.draw()
            
    def resume(self):
        loop = pyglet.media.SourceGroup(audio_levels["GAME"].audio_format if states["GAME"].current_level != 8 else audio_format["LAST"].audio_format, None)
        loop.loop = True
        loop.queue(audio_levels["MENU"] if states["GAME"].current_level != 8 else audio_format["LAST"])
        speaker.queue(loop)
        speaker.next_source()
        return "GAME"
    
    def replay_level(self):
        states["GAME"].replay_level()
        loop = pyglet.media.SourceGroup(audio_levels["GAME"].audio_format if states["GAME"].current_level != 8 else audio_format["LAST"].audio_format, None)
        loop.loop = True
        loop.queue(audio_levels["GAME"] if states["GAME"].current_level != 8 else audio_format["LAST"])
        speaker.queue(loop)
        speaker.next_source()
        return "GAME"
        
    def new_game(self):
        states["GAME"].new_game()
        states["TALE"].set_level_score(0, 3)
        loop = pyglet.media.SourceGroup(audio_levels["TALE"].audio_format, None)
        loop.loop = True
        loop.queue(audio_levels["TALE"])
        speaker.queue(loop)
        speaker.next_source()
        return "TALE"
    def save(self):
        print("last {}".format(states["GAME"].current_level))
        with open("last", "w") as fi:
            fi.write(str(states["GAME"].current_level - 1))
        pyglet.app.exit()

class TaleState:
    def __init__(self):
        self.level = last
        self.score = 3
        self.scene = pyglet.sprite.Sprite(pyglet.resource.image(os.path.join("graphics", "scene1.png")), x = 0, y = 0)
        texts = [("Ahma'Treta'ji bud na teba milostivá. Aghe chcú si ovládat svet, kým my sme spali. Musíme získat spät našu vládu a našu rísu. Je to na tebe, azma'Amaz'haja. Nech Ahma'Treta'ji sprevádza tvoje posledné kroky na tejto znesvätenej zemi a zober zo sebou, tých čo znesvätili, tolko kolko môzes. Ó Ahma'Treta'ji, nech bdie nad tebou. ASDW uzívaj na hýbanie a enterom finálnym odpál sa do nebies. Lez pamätaj tolko, musíš kamuflovat sa, k farebnému rovnakým odevom.", "Nech Ahma'Treta'ji príjme moju obetu, ahma'Amaz'keu"),
                 ("Tvoja sestra zlyhala! Ahma'Treta'ji sa velmi v nebesiac mracit musí, jej bojovnícka zomrela, ale aghe zo sebou, tých nevzala! ci nebola v pakte s nimi, nehanebná? Preto ty, azma'Amaz'legha musís dokonat jej úlohu.", "Nech Ahma'Treta'ji stojí nad nami, ved ako v ahma'Knihe stojí, aghe nenechat nazive, ak mozno!"), ("Tvoja sestra zlyhala! Ahma'Treta'ji sa velmi v nebesiac mracit musí, jej bojovnícka zomrela, ale aghe zo sebou, tých nevzala! ci nebola v pakte s nimi, nehanebná? Preto ty, azma'Amaz'legha musís dokonat jej úlohu.", "Nech Ahma'Treta'ji stojí nad nami, ved ako v ahma'Knihe stojí, aghe nenechat nazive, ak mozno!"), ("Ahma'Treta'ji, cím trestá nás ked nehodné bojovnice idú do boja?! Ty nesklam ju, azma'Amaz'eque a bude tvoje miesto pri nej. Pozoruj tých aghe, hlúpi sú, zosúlad ich a odpál sa do nebies.", "Nech Ahma'Treta'ji chystá miesto pri nej!"), ("Azma'Amaz'dela, tvoja sestra uspela! Nech i teba Ahma'Treta'ji sprevádza. Ostali v mest dve skupiny aghe, spoj ich a znic, Ahma'Treta'ji ta pozehná. No pozor si daj aby zapadla do mesta, nech v pokoji vykonás svoju úlohu!", "Ako Ahma'Treta'ji káze, veleknazka."), ("Tvoja sestra zlyhala! Ahma'Treta'ji sa velmi v nebesiac mracit musí, jej bojovnícka zomrela, ale aghe zo sebou, tých nevzala! ci nebola v pakte s nimi, nehanebná? Preto ty, azma'Amaz'legha musís dokonat jej úlohu.", "Nech Ahma'Treta'ji stojí nad nami, ved ako v ahma'Knihe stojí, aghe nenechat nazive, ak mozno!"), ("Tvoja sestra zlyhala! Ahma'Treta'ji sa velmi v nebesiac mracit musí, jej bojovnícka zomrela, ale aghe zo sebou, tých nevzala! ci nebola v pakte s nimi, nehanebná? Preto ty, azma'Amaz'legha musís dokonat jej úlohu.", "Nech Ahma'Treta'ji stojínad nami, ved ako v ahma'Knihe stojí, aghe nenechat nazive, ak mozno!"), ("Ahma'Treta'ji, cím trestá nás ked nehodné bojovnice idú do boja?! Ty nesklam ju, azma'Amaz'eque a bude tvoje miesto pri nej. Pozoruj tých aghe, hlúpi sú, zosúlad ich a odpál sa do nebies.", "Nech Ahma'Treta'ji chystá miesto pri nej!"), ("Aghe, pliaga tohto sveta zacali organizovat sa, ved Ahma'Treta'ji ich strestá. Bola si dobrou bojovníckou v jej radoch, ale musíme proti nim inaksie zakrocit! Treba zabit ich lídra, nech rozpŕchnu sa zberba! A zober ich co najviac s ním, azma'Amaz'jada!", "cierne vlasy, líder aghe, zobrat do ho pekiel podzemných. Ahma'Treta'ji, idem za tebou!"), ("Tvoja sestra zlyhala! Ahma'Treta'ji sa velmi v nebesiac mracit musí, jej bojovnícka zomrela, ale aghe zo sebou, tých nevzala! ci nebola v pakte s nimi, nehanebná? Preto ty, azma'Amaz'legha musís dokonat jej úlohu.", "Nech Ahma'Treta'ji stojí nad nami, ved ako v ahma'Knihe stojí, aghe nenechat nazive, ak mozno!"),
                 ("Azma! Tvoja sestra nedobre pocúvala, ci spolcit sa s nimi? zeby jej líder aghe ucaroval, previnila sa hriechom proti ahma'Knihe a nasej bohyni? Ahma'Treta'ji zlutuj sa nad nami, posielam dalsiu zvládnut misiu. Lídra aghe treba skántrit, azma'Amaz'gera.", ""), ("Nikoho nezobrala zo sebou, a oni, aghe, dohodli sa, nového lídra majú! Znic ho, pri Ahma'Treta'ji!", ""), ("Azma'Amaz'Lena, jedna nasa sestra, azma'Amaz'corle je v meste, musíte tú nezbubit, inak Ahma'Treta'ji rozdrví svojím hnevom nase múry, bez zmyslu nezhubís Amaz'hanu! Ale daj napozor si, azma', bo v tomto meste výbuchy sa daleko síria, aspon tri kamene medzi sebou, nech sluzobnici Ahma'Treta'ji nic nestane sa!", "Ako Ahma'Treta'ji zelá's tak nech stane sa."), ("Zabila len svoju sestru, hnev na nás presvätá znesie! Rýchlo chod napravit to, kým jej'z hnev sa roznesie!", "Ach aghe'uz-nie-sestra, co to spravila, musíme rýchlo aghe' zbavit sa!"), ("Tvoja sestra zlyhala! Ahma'Treta'ji sa velmi v nebesiac mracit musí, jej bojovnícka zomrela, ale aghe zo sebou, tých nevzala! ci nebola v pakte s nimi, nehanebná? Preto ty, azma'Amaz'legha musís dokonat jej úlohu.", "Nech Ahma'Treta'ji stojí nad nami, ved ako v ahma'Knihe stojí, aghe nenechat nazive, ak mozno!"), ("Pri Ahma'Treta'ji, zahubila sluzobnicu! Nech hanba nad nou je, pomer dva ku jednej, pozehnané sestry a aghe, toto nemôzeme Ahma'Treta'ji dopustit! Aký hnev bude mat na nás! Noze naprav sestry chybu, daleko od sestry nasej mri.", "Amha'Amaz'corle neskrivím ani drahokam na hlave, pri Ahma'Treta'ji."), ("Azma'Amaz'maie, do nového mesta musís íst. V tomto meste dvaja aghe, ale nemôzeme len tak zabíjat sa k nim. Nastastie, Ahma'Treta'ji nám pozehnala. V skrini nájdes vestu si a z nej aghe-lamutiace prekázky môzes nosit. Len ich poloz na miesto, Enterom ich daj na dlázku a ich to zastaví pliagu! Len pozor si daj, Azma'Amaz'maie, ked más tú vestu, tak tvoje náloze nebuchnú!", "Ahma'Treta'ji nám pozehnáva a sád s týmto darom lahko sa oboch zbavím!"),
                 ("Tvoja sestra zlyhala! Ahma'Treta'ji sa velmi v nebesiac mracit musí, jej bojovnícka zomrela, ale aghe zo sebou, tých nevzala! ci nebola v pakte s nimi, nehanebná? Preto ty, azma'Amaz'legha musís dokonat jej úlohu.", "Nech Ahma'Treta'ji stojí nad nami, ved ako v ahma'Knihe stojí, aghe nenechat nazive, ak mozno!"), ("Tvoja sestra zlyhala! Ahma'Treta'ji sa velmi v nebesiac mracit musí, jej bojovnícka zomrela, ale aghe zo sebou, tých nevzala! ci nebola v pakte s nimi, nehanebná? Preto ty, azma'Amaz'legha musís dokonat jej úlohu.", "Nech Ahma'Treta'ji stojí nad nami, ved ako v ahma'Knihe stojí, aghe nenechat nazive, ak mozno!"), ("Ahma'Treta'ji, cím trestá nás ked nehodné bojovnice idú do boja?! Ty nesklam ju, azma'Amaz'eque a bude tvoje miesto pri nej. Pozoruj tých aghe, hlúpi sú, zosúlad ich a odpál sa do nebies.", "Nech Ahma'Treta'ji chystá miesto pri nej!"), ("Postupujeme, ako dobre, ako dobre. Ahma'Treta'ji stojí nad nami, vyhubíme aghe! Len treba poctivo plnovat, ako nám Ahma'Treta'ji dala do vienka. V skrini na okraji mesta nájdes zelenú výstroj. Z tej vybrat dajú sa také predmety ktoré zvedavost, hlúpu veru, indukujú. Aghe vidia ju, otocia sa hned. Vyuzi to, vyuzi to, ty na svoj prospech!", ""), ("Tvoja sestra zlyhala! Ahma'Treta'ji sa velmi v nebesiac mracit musí, jej bojovnícka zomrela, ale aghe zo sebou, tých nevzala! ci nebola v pakte s nimi, nehanebná? Preto ty, azma'Amaz'legha musís dokonat jej úlohu.", "Nech Ahma'Treta'ji stojí nad nami, ved ako v ahma'Knihe stojí, aghe nenechat nazive, ak mozno!"), ("Jeden?! Ahma'Treta'ji, ci v chrámoch múdre a schopné nevedieme? Tak ako koza zelenov stojí, aghe nás nesmú prelstit - to my ich!", ""), ("Dvaja? Ahma'Kniha zatracuje sestry tvojej konanie. Naprav to!", ""), ("Vyvinút sa, s pozehnaním velkej a mocnej Ahma'Treta'ji, vyvinút zbran. Táto bomba nezabíja na dialku, lez vsetci, ku ktorým sa vie dostat blesk, len cez skrine a prázdne polia, toho oni zahubia. Sú tam ale tvoje sestry, tie nenechaj zhynút, iba ty más dnes dosiahnut nebesá!", "Stane sa."), ("Dve sestry zabila, vecná jej hanba. Spolu aj s aghe, do pekiel tiahla!"), ("Zabila sestru svoju, hanba jej a hnev Ahma'Treta'ji! Viac sa snaziz musís ako tvoja sestra, aby dostala potom miesto v jej pri jej oltári!", ""), ("Málo obetí nevestí miesto pri jej boku!", ""), ("Ahma'Treta'ji, tak dopriala si mi vidiet tento pohlad. Vyhrali sme, ale len temer. Aghe, aká nedobrá sila im pomohla, sami by iste nezvládli to! Ked prejdes popri skrini ciernavy, plachta ciara na teba sa zavalí! Uz tak zhynuli a nezvládli obetu svoju, lez ty na to pozor daj a maj sa k boju. Pozeraj sa dobre, co aghe robia, ved sú oni hlúpi!", "Ahma'Amaz'keu, vdaka ti za sancu. Pri Ahma'Treta'ji skoncit chcem, nech oni zit ani len nezacnú!"), ("Prezilo ich vela, tvoja sestra tela!", ""), ("V tme sa musís orientovat, pamät dobrú vlastnit. Aghe síce hlúpi sú, ale neprestanú s' cyklit!", ""), ("Takmer k cielu dosiahla tvoja sestra, ale musís dokázat znicit vsetkých. Bo i ked zomreli dalsí sa hrnú. Mysia si ze bezpecne, mi prejeme im cez rozum! Ahma'Treta'ji, posledná skúska!", "Bude mi ctou."), ("Dokonané. Sestry, vyhrali sme! Nech nás rod vládne!", "A Ahma'Treta'ji nad nami.")]
        
        
        self.replicas = []
        for text in texts:
            
            limit = 45
            self.replicas.append(([""], [""]))
            for word in text[0].split():
                print("{} a {}".format(self.replicas[-1][0][-1], word))
                print("len {} + {} < {}".format(len(self.replicas[-1][0][-1]), len(word), limit))
                if len(self.replicas[-1][0][-1]) + len(word) < limit:
                    self.replicas[-1][0][-1] += " " + word
                else:
                    self.replicas[-1][0].append(word)
            limit = 30
            for word in text[1].split():
                print("{} a {}".format(self.replicas[-1][1][-1], word))
                print("len {} + {} < {}".format(len(self.replicas[-1][1][-1]), len(word), limit))
                if len(self.replicas[-1][1][-1]) + len(word) < limit:
                    self.replicas[-1][1][-1] += " " + word
                else:
                    self.replicas[-1][1].append(word)
        print(self.replicas)
        self.keu = [pyglet.text.Label(self.replicas[(self.level - 1) * 4 + 1 + self.score][0][i], font_name = 'Cardinal', font_size = 23, anchor_x = 'center', anchor_y = 'center', x = width // 2 + 200, y = height - 30 - i * 50) for i in range(len(self.replicas[(self.level - 1) * 4 + 1 + self.score][0]))]
        self.sec = [pyglet.text.Label(self.replicas[(self.level - 1) * 4 + 1 + self.score][1][i], font_name = 'Cardinal', font_size = 23, anchor_x = 'center', anchor_y = 'center', x = width // 2 - 300, y = 450 - i * 50, color = (0, 0, 0, 255)) for i in range(len(self.replicas[(self.level - 1) * 4 + 1 + self.score][1]))]
            
    def update(self, dt):
        return "TALE"
    
    def key_press(self, key):
        if self.score == 3 and self.level != 0:
            states["GAME"].next_level()
        else:
            states["GAME"].replay_level()
        loop = pyglet.media.SourceGroup(audio_levels["GAME"].audio_format if states["GAME"].current_level != 8 else audio_format["LAST"].audio_format, None)
        loop.loop = True
        loop.queue(audio_levels["GAME"] if states["GAME"].current_level != 8 else audio_format["LAST"])
        speaker.queue(loop)
        speaker.next_source()
        return "GAME"
    
    def draw(self):
        self.scene.draw()
        for label in self.keu:
            label.draw()
        for label in self.sec:
            label.draw()
    
    def set_level_score(self, level, score):
        self.level = level
        self.score = score
        print("Som v leveli {}".format(level))
        self.keu = [pyglet.text.Label(self.replicas[(self.level - 1) * 4 + 1 + self.score][0][i], font_name = 'Cardinal', font_size = 23, anchor_x = 'center', anchor_y = 'center', x = width // 2 + 200, y = height - 30 - i * 50) for i in range(len(self.replicas[(self.level - 1) * 4 + 1 + self.score][0]))]
        self.sec = [pyglet.text.Label(self.replicas[(self.level - 1) * 4 + 1 + self.score][1][i], font_name = 'Cardinal', font_size = 23, anchor_x = 'center', anchor_y = 'center', x = width // 2 - 300, y = 450 - i * 50, color = (0, 0, 0, 255)) for i in range(len(self.replicas[(self.level - 1) * 4 + 1 + self.score][1]))]
        
states = {"GAME" : GameState(),
          "WIN" : WinState(),
          "MENU" : MenuState(), 
          "TALE" : TaleState()}


current = "MENU"



@window.event
def on_draw():
    global current
    window.clear()
    states[current].draw()
    
@window.event
def on_key_press(symbol, modifiers):
    global current
    print("key he {} a current {}".format(symbol, current))
    if symbol == pyglet.window.key.ESCAPE:
        loop = pyglet.media.SourceGroup(audio_levels["MENU"].audio_format, None)
        loop.loop = True
        loop.queue(audio_levels["MENU"])
        speaker.queue(loop)
        speaker.next_source()
        current = "MENU"
        return pyglet.event.EVENT_HANDLED
    if not symbol in pressed.keys():
        print("Neni")
        return None
    if pressed[symbol]: 
        pass
    else:
        pressed[symbol] = True
        current = states[current].key_press(symbol)
        print("current {}".format(current))


@window.event
def on_key_release(symbol, modifiers):
    pressed[symbol] = False

accum = 0

def update(dt):
    global current, accum
    accum += dt
    
    while accum >= STEP:
        current = states[current].update(STEP)
        accum -= STEP
    window.set_caption("Vzostup Amaz'hán [" + str(int(1 / dt)) + "]")

pyglet.clock.schedule_interval(update, 1 / FPS)

pyglet.app.run()
