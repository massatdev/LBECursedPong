#import game
import random

class CurseManager:
    def __init__(self):
        self.active_curses = set()
        self.duration = 0

        self.curses = {
            "INVERT_CONTROLS": "You suddenly feel disoriented.\nWhich way is right?",
            "PALPITATIONS": "You feel your heart pounding out of your chest\nAre you just anxious, or is it a dark omen?.",
            "SHAKY_HANDS": "Your hands now seem to have a mind of their own,\nno longer abiding your command directly.",
            "FATIGUE": "You feel exhausted. Has it been that long?",
            "STROKE_L": "Your left side feels numb.\nYou can't feel your left arm or leg anymore.",
            "STROKE_R": "Your right side feels numb.\nYou can't feel your right arm or leg anymore.",
            "SLEEPY": "You feel like you can fall asleep at any moment.\nWhen was the last time you closed your eyes?",
        }

        self.notcurse = False
        self.notcurse_text = "You feel a now unfamiliar sense of relief.\nIt seems that whatever was watching finally left you for now.\nBut have you truly escaped?"

        self.blackout_timer = 0
        self.blackout_cooldown = random.randint(60, 300)  # cooldown duration in frames

        self.notice_text = "Against your better judgement,\nyou decided to descend into the depths of the cursed pong.\nYou feel like something is wagering on your failure.\nIs it even possible to win this game?"
        self.notice_timer = 300

    def trigger_random_curse(self, level):
        unused_curses = [c for c in self.curses if c not in self.active_curses]

        if level > 6:
            self.active_curses.clear()
            self.notice_text = self.notcurse_text
            self.notice_timer = 300
            self.notcurse = True
            print("WELL PLAYED, FOR NOW...")
            return None

        if unused_curses:
            chosen = random.choice(unused_curses)
            self.active_curses.add(chosen)
            self.notice_text = f"{self.curses[chosen]}"
            self.notice_timer = 180
            
            print(f"NEW CURSE: {chosen}")
            return chosen
        return None

    def has_curse(self, curse_name):
        return curse_name in self.active_curses

    def update(self):
        if self.has_curse("SLEEPY"):
            if self.blackout_timer > 0:
                self.blackout_timer -= 1
            else:
                self.blackout_cooldown -= 1
                if self.blackout_cooldown <= 0:
                    self.blackout_timer = random.randint(30, 300) # blackout duration in frames       
                    self.blackout_cooldown = random.randint(300, 1800) # cooldown duration in frames

        if self.notice_timer > 0:
            self.notice_timer -= 1

    def is_blackout(self):
        return self.has_curse("SLEEPY") and self.blackout_timer > 0

    def draw_menacing_text(self, screen, font, width, height):
        if self.notice_timer > 0:
            if not self.notcurse:
                shake_x = random.randint(-3, 3)
                shake_y = random.randint(-3, 3)
            else:
                shake_x = 0
                shake_y = 0

            lines = self.notice_text.split('\n')
            
            line_height = font.get_linesize()
            total_height = len(lines) * line_height
            
            start_y = (height // 2) - (total_height // 2) + shake_y

            for i, line in enumerate(lines):
                if self.notcurse:
                    text_surface = font.render(line, True, (13, 71, 161))
                    shadow_surface = font.render(line, True, (0, 0, 0))
                else:
                    text_surface = font.render(line, True, (109, 8, 8)) 
                    shadow_surface = font.render(line, True, (45, 0, 0)) 

                text_rect = text_surface.get_rect(center=(width // 2 + shake_x, start_y + (i * line_height)))
                shadow_rect = shadow_surface.get_rect(center=(width // 2 + shake_x + 3, start_y + (i * line_height) + 3))

                screen.blit(shadow_surface, shadow_rect)
                screen.blit(text_surface, text_rect)

    def reset(self):
        self.active_curses.clear()
        self.blackout_timer = 0
        self.blackout_cooldown = random.randint(60, 300)  # cooldown duration in frames
        self.notice_timer = 0