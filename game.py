import simplegui, math, random
ghostSprites = simplegui.load_image('https://github.com/TheoF-B/Super-Bash-Bros/blob/main/assets/Ghost%20Sheet.png?raw=true')
brawlerSprites = simplegui.load_image('https://github.com/TheoF-B/Super-Bash-Bros/blob/main/assets/Brawler%20Sheet.png?raw=true')
swordieSprites = simplegui.load_image('https://github.com/TheoF-B/Super-Bash-Bros/blob/main/assets/Swordfighter%20Sheet.png?raw=true')
stage = simplegui.load_image('https://github.com/TheoF-B/Super-Bash-Bros/blob/main/assets/Stage.png?raw=true')
titleScreen = simplegui.load_image('https://github.com/TheoF-B/Super-Bash-Bros/blob/main/assets/Title%20Screen.png?raw=true')
# The Vector class
class Vector:

    # Initialiser
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # Returns a string representation of the vector
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    # Tests the equality of this vector and another
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # Tests the inequality of this vector and another
    def __ne__(self, other):
        return not self.__eq__(other)

    # Returns a tuple with the point corresponding to the vector
    def get_p(self):
        return (self.x, self.y)

    # Returns a copy of the vector
    def copy(self):
        return Vector(self.x, self.y)

    # Adds another vector to this vector
    def add(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __add__(self, other):
        return self.copy().add(other)

    # Negates the vector (makes it point in the opposite direction)
    def negate(self):
        return self.multiply(-1)

    def __neg__(self):
        return self.copy().negate()

    # Subtracts another vector from this vector
    def subtract(self, other):
        return self.add(-other)

    def __sub__(self, other):
        return self.copy().subtract(other)

    # Multiplies the vector by a scalar
    def multiply(self, k):
        self.x *= k
        self.y *= k
        return self

    def __mul__(self, k):
        return self.copy().multiply(k)

    def __rmul__(self, k):
        return self.copy().multiply(k)

    # Divides the vector by a scalar
    def divide(self, k):
        return self.multiply(1/k)

    def __truediv__(self, k):
        return self.copy().divide(k)

    # Normalizes the vector
    def normalize(self):
        return self.divide(self.length())

    # Returns a normalized version of the vector
    def get_normalized(self):
        return self.copy().normalize()

    # Returns the dot product of this vector with another one
    def dot(self, other):
        return self.x * other.x + self.y * other.y

    # Returns the length of the vector
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    # Returns the squared length of the vector
    def length_squared(self):
        return self.x**2 + self.y**2

    # Reflect this vector on a normal
    def reflect(self, normal):
        n = normal.copy()
        n.multiply(2*self.dot(normal))
        self.subtract(n)
        return self

    # Returns the angle between this vector and another one
    def angle(self, other):
        return math.acos(self.dot(other) / (self.length() * other.length()))

    # Rotates the vector 90 degrees anticlockwise
    def rotate_anti(self):
        self.x, self.y = -self.y, self.x
        return self

    # Rotates the vector according to an angle theta given in radians
    def rotate_rad(self, theta):
        rx = self.x * math.cos(theta) - self.y * math.sin(theta)
        ry = self.x * math.sin(theta) + self.y * math.cos(theta)
        self.x, self.y = rx, ry
        return self

    # Rotates the vector according to an angle theta given in degrees
    def rotate(self, theta):
        theta_rad = theta / 180 * math.pi
        return self.rotate_rad(theta_rad)
    
    # project the vector onto a given vector
    def get_proj(self, vec):
        unit = vec.get_normalized()
        return unit.multiply(self.dot(unit))

WIDTH = 800
HEIGHT = 500
GRAVITY = Vector(0, 1)

class AI:

    def __init__(self, pos = Vector(400, 350)):
        #pos here refers to the centre of the character
        self.spritesheet = Spritesheet(ghostSprites, 4, 12, 42, 0, 0, 0, 64, 64, [0,0])
        self.pos = pos
        self.vel = Vector(0,0)
        self.left = False
        self.frame_count = 0
        self.index = [0,0]
        self.attack = False
        self.hitbox = []
        self.hurtbox = collision_box("line", [self.pos + Vector(0,23), self.pos + Vector(0, -21)], 24)


    def draw(self, canvas):
        horizIndex = self.index[0]
        verticIndex = self.index[1]
        if self.left:
            horizIndex += 6
        self.spritesheet.draw2(canvas, horizIndex, verticIndex, self.pos)

    def update(self, player_pos):### give player position as a vector find vector from AI to player then move towards player
        self.pos += self.vel
        self.hurtbox.changeCoords([self.pos + Vector(0,23), self.pos + Vector(0, -21)])
        self.frame_count = (self.frame_count + 1) % 5
        if not self.attack:
            direction = player_pos - self.pos
            
            if direction.x > 0:
                self.left = False
            else:
                self.left = True

            if direction.length() < 50:
                self.Attack()
        
            elif self.frame_count == 0:
                self.vel = 3 * direction.get_normalized()
                self.index[0] = (self.index[0] + 1) % 4
        
        else: 
            if self.frame_count == 0 or self.frame_count == 4 or self.frame_count == 2:
                self.index[0] = (self.index[0] + 1) % 6
                if self.index[0] == 0:
                    self.index[1] += 1
                
                if (self.index[0] == 5) and (self.index[1] == 3):
                    self.attack = False
                    self.index = [0,0]

                if (self.index[0] == 1) and (self.index[1] == 2): ### part of the animation where the hitbox should come out
                    if self.left:
                        self.hitbox.append(Hitbox(self.pos + Vector(-16, -7), 16, 14))
                    else:
                        self.hitbox.append(Hitbox(self.pos + Vector(16, -7), 16, 14))
                elif (self.index[0] == 2) and (self.index[1] == 2):
                    if self.left:
                        self.hitbox[0] = Hitbox(self.pos + Vector(-18, 4), 14, 20)
                    else:
                        self.hitbox[0] = Hitbox(self.pos + Vector(18, 4), 14, 20)
                elif (self.index[0] == 4) and (self.index[1] == 2):
                    self.hitbox.clear()


    def Attack(self):  
        self.vel = Vector(0,0)
        self.attack = True
        self.frame_count = 0
        self.index = [0, 1]
class Clock:
    def __init__(self, ptime):
        self.time = ptime
        
    def tick(self):
        self.time += 1
        
    def transition(self, frame_duration):
        Clock.tick(self)
        if self.time % frame_duration == 0:
            return True
        return False
class Character:

    def __init__(self, pos = Vector(0, 0),
    vel = Vector(0, 0),
    height = 80,
    width = 80,
    thickness = 5):
        #pos here refers to the centre of the character
        self.pos = pos
        self.height = height
        self.width = width
        self.sprite_width = height
        self.sprite_height = width
        self.sprite = Spritesheet(brawlerSprites, 5, 12, 60, self.pos.x, self.pos.y, 60, self.sprite_height, self.sprite_width, [0, 0])
        self.vel = vel
        self.thickness = thickness
        self.floor_collision = collision_box("circle", self.pos + Vector(0, self.height/2), 10)
        self.hurt_box = collision_box("line", [self.pos + Vector(0, self.height / 2), self.pos + Vector(0, - self.height / 2)], self.width/3)
        self.hitbox = []
        self.grounded = True
        self.lives = 3
        self.charType = "Brawler"
        self.left = False
        self.in_collision = False
        self.light = False
        self.heavy = False
        self.frame_count = 0
        self.index = [0,0]
        self.damage = 0
        

    def get_corners(self, position):
        bot_left = position.get_p()
        bot_right = (bot_left[0] + self.width, bot_left[1])
        top_left = (bot_left[0], bot_left[1] - self.height)
        top_right = (bot_right[0], bot_right[1] - self.height)

        return [bot_left, bot_right, top_right, top_left]

    def collision(self, other_box):
        return self.floor_collision.collide(other_box)

    def draw(self, canvas):
        horizIndex = self.index[0]
        verticIndex = self.index[1]
        if self.left:
            horizIndex += 6
        self.sprite.draw2(canvas, horizIndex, verticIndex, self.pos)
        #self.floor_collision.draw(canvas, 'Red')
        #self.hurt_box.draw(canvas, 'Yellow')

    def update(self, Gravity, other_boxes):
        self.frame_count = (self.frame_count + 1) % 5
        self.in_collision = False
        self.grounded = False
    
        for c_box in other_boxes:
            if self.collision(c_box):
                self.in_collision =  True
                
                if isinstance(c_box, PlatformBox):
                    self.grounded = True
                    if self.vel.y > 0:#self.floor_collision.coordinates.y > c_box.floor_height:
                        self.pos.y = c_box.floor_height - (self.height / 2) + 1
                    if self.vel.y > 0:
                        self.vel.y = 0
                else:
                    self.pos = self.pos - 3 * c_box.width * c_box.direction
                    self.vel = self.vel - 2 * self.vel.get_proj(c_box.direction)

        if not self.grounded:
            self.vel.add(Gravity)
        
        if self.vel.y < -15:
            self.vel.y = -15
        elif self.vel.y > 15:
            self.vel.y = 15
        self.pos.add(self.vel)
        self.floor_collision.changeCoords(self.pos + Vector(0, self.height / 2))
        self.hurt_box.changeCoords([self.pos + Vector(0, self.height / 2), self.pos + Vector(0, - self.height / 2)])
        self.sprite.posX = self.pos.x
        self.sprite.posY = self.pos.y
        self.vel.x *= 0.75
        if self.light:
            self.AttackingBrawlLight()

    def die(self):
        self.lives -= 1
        self.pos = Vector(400, 200)
        self.vel = Vector(0,0)
        self.damage = 0
    

    def Idle(self):
        self.index = [0,0]

        #self.sprite = Spritesheet( "https://i.ibb.co/6BktkVR/idle-modified.png", 1, 1, 1, self.pos.x, self.pos.y, 12, self.sprite_height, self.sprite_width, 0)
    def Running(self):
        self.index[1] = 1
        if self.frame_count == 0:
            self.index[0] = (self.index[0] + 1) % 6
        
        #self.sprite = Spritesheet("https://i.ibb.co/6ymMDRp/running.png", 3, 4, 6, self.pos.x, self.pos.y, 12, self.sprite_height, self.sprite_width, pFrameIndex)
    def AttackingBrawlLight(self):
        self.index[1] = 4
        if not self.light:
            self.light = True
            self.index[0] = 0
        elif self.light and (self.frame_count == 0 or self.frame_count == 3):
            if self.left and self.index[0] == 0:
                self.hitbox.append(Hitbox(self.pos + Vector(-9, 7), 20, 15, 0))
            elif not self.left and self.index[0] == 0:
                self.hitbox.append(Hitbox(self.pos + Vector(9, 7), 20, 15, 0))
            elif self.index[0] == 5:
                self.hitbox.clear()
                self.light = False
            self.index[0] = (self.index[0] + 1) % 6
        

        
        #self.sprite = Spritesheet( "https://i.ibb.co/PwzMfFj/brawl-Attack.png", 6, 2, 6, self.pos.x, self.pos.y, 12, self.sprite_height, self.sprite_width, pFrameIndex)
    #def AttackingSwordLight(self, pFrameIndex):
    #    self.sprite = Spritesheet( "", , , , self.pos.x, self.pos.y, 12, self.height, self.width, pFrameIndex)
    def AttackingBrawlHeavy(self, pFrameIndex):
        pass

        #self.sprite = Spritesheet( "https://i.ibb.co/PwzMfFj/brawl-Attack.png", 6, 2, 6, self.pos.x, self.pos.y, 18, self.sprite_height, self.sprite_width, pFrameIndex)
    #def AttackingSwordHeavy(self, pFrameIndex):
    #    self.sprite = Spritesheet( "", , , , self.pos.x, self.pos.y, 12, self.height, self.width, pFrameIndex)
    def Crouching(self):
        self.index[1] = 3
        if self.frame_count == 0:
            if self.index[0] != 5:
                self.index[0] = (self.index[0] + 1)
        #self.sprite = Spritesheet( "https://i.ibb.co/fqLFpBZ/Crouching.png", 3, 4, 6, self.pos.x, self.pos.y, 12, self.sprite_height, self.sprite_width, pFrameIndex)
    def Jumping(self):
        self.index[1] = 2
        if self.frame_count == 0:
            if self.index[0] != 5:
                self.index[0] = (self.index[0] + 1)
class SwordCharacter:

    def __init__(self, pos = Vector(0, 0),
    vel = Vector(0, 0),
    height = 80,
    width = 80,
    thickness = 5):
        #pos here refers to the centre of the character
        self.pos = pos
        self.height = height
        self.width = width
        self.sprite_width = height
        self.sprite_height = width
        self.sprite = Spritesheet(swordieSprites, 5, 12, 60, self.pos.x, self.pos.y, 60, self.sprite_height, self.sprite_width + 32, [0, 0])
        self.vel = vel
        self.thickness = thickness
        self.floor_collision = collision_box("circle", self.pos + Vector(0, self.height/2), 10)
        self.hurt_box = collision_box("line", [self.pos + Vector(0, self.height / 2), self.pos + Vector(0, - self.height / 2)], self.width/3)
        self.hitbox = []
        self.grounded = True
        self.lives = 3
        self.damage = 0
        self.charType = "Sword"
        self.left = False
        self.in_collision = False
        self.light = False
        self.heavy = False
        self.frame_count = 0
        self.index = [0,0]
        

    def get_corners(self, position):
        bot_left = position.get_p()
        bot_right = (bot_left[0] + self.width, bot_left[1])
        top_left = (bot_left[0], bot_left[1] - self.height)
        top_right = (bot_right[0], bot_right[1] - self.height)

        return [bot_left, bot_right, top_right, top_left]

    def collision(self, other_box):
        return self.floor_collision.collide(other_box)

    def draw(self, canvas):
        horizIndex = self.index[0]
        verticIndex = self.index[1]
        if self.left:
            horizIndex += 6
        self.sprite.draw2(canvas, horizIndex, verticIndex, self.pos)
        #self.floor_collision.draw(canvas, 'Red')
        #self.hurt_box.draw(canvas, 'Yellow')
        #for hitbox in self.hitbox:
            #hitbox.draw(canvas, 'Red')

    def update(self, Gravity, other_boxes):
        self.frame_count = (self.frame_count + 1) % 6
        self.in_collision = False
        self.grounded = False
    
        for c_box in other_boxes:
            if self.collision(c_box):
                self.in_collision =  True
                
                if isinstance(c_box, PlatformBox):
                    self.grounded = True
                    if self.vel.y > 0:#self.floor_collision.coordinates.y > c_box.floor_height:
                        self.pos.y = c_box.floor_height - (self.height / 2) + 1
                    if self.vel.y > 0:
                        self.vel.y = 0
                else:
                    self.pos = self.pos - 3 * c_box.width * c_box.direction
                    self.vel = self.vel - 2 * self.vel.get_proj(c_box.direction)

        if not self.grounded:
            self.vel.add(Gravity)
        
        if self.vel.y < -15:
            self.vel.y = -15
        elif self.vel.y > 15:
            self.vel.y = 15
        self.pos.add(self.vel)
        self.floor_collision.changeCoords(self.pos + Vector(0, self.height / 2))
        self.hurt_box.changeCoords([self.pos + Vector(0, self.height / 2), self.pos + Vector(0, - self.height / 2)])
        self.sprite.posX = self.pos.x
        self.sprite.posY = self.pos.y
        self.vel.x *= 0.75
        if self.light:
            self.AttackingSwordLight()

    def die(self):
        self.lives -= 1
        self.pos = Vector(400, 200)
        self.vel = Vector(0,0)
        self.damage = 0
    

    def Idle(self):
        self.index = [0,0]

        #self.sprite = Spritesheet( "https://i.ibb.co/6BktkVR/idle-modified.png", 1, 1, 1, self.pos.x, self.pos.y, 12, self.sprite_height, self.sprite_width, 0)
    def Running(self):
        self.index[1] = 1
        if self.frame_count == 0:
            self.index[0] = (self.index[0] + 1) % 6
        
        #self.sprite = Spritesheet("https://i.ibb.co/6ymMDRp/running.png", 3, 4, 6, self.pos.x, self.pos.y, 12, self.sprite_height, self.sprite_width, pFrameIndex)
    def AttackingSwordLight(self):
        self.index[1] = 4
        if not self.light:
            self.light = True
            self.index[0] = 0
        elif self.light and (self.frame_count == 0 or self.frame_count == 3):
            if self.left and self.index[0] == 2:
                self.hitbox.append(Hitbox(self.pos + Vector(-30, 2), 17, 15, 0))
            elif not self.left and self.index[0] == 2:
                self.hitbox.append(Hitbox(self.pos + Vector(30, 2), 17, 15, 0))
            elif self.index[0] == 4:
                self.hitbox.clear()
            elif self.index[0] == 5:
                self.light = False
            self.index[0] = (self.index[0] + 1) % 6
        

        
        #self.sprite = Spritesheet( "https://i.ibb.co/PwzMfFj/brawl-Attack.png", 6, 2, 6, self.pos.x, self.pos.y, 12, self.sprite_height, self.sprite_width, pFrameIndex)
    #def AttackingSwordLight(self, pFrameIndex):
    #    self.sprite = Spritesheet( "", , , , self.pos.x, self.pos.y, 12, self.height, self.width, pFrameIndex)
    def AttackingSwordHeavy(self, pFrameIndex):
        pass

        #self.sprite = Spritesheet( "https://i.ibb.co/PwzMfFj/brawl-Attack.png", 6, 2, 6, self.pos.x, self.pos.y, 18, self.sprite_height, self.sprite_width, pFrameIndex)
    #def AttackingSwordHeavy(self, pFrameIndex):
    #    self.sprite = Spritesheet( "", , , , self.pos.x, self.pos.y, 12, self.height, self.width, pFrameIndex)
    def Crouching(self):
        self.index[1] = 3
        if self.frame_count == 0:
            if self.index[0] != 5:
                self.index[0] = (self.index[0] + 1)
        #self.sprite = Spritesheet( "https://i.ibb.co/fqLFpBZ/Crouching.png", 3, 4, 6, self.pos.x, self.pos.y, 12, self.sprite_height, self.sprite_width, pFrameIndex)
    def Jumping(self):
        self.index[1] = 2
        if self.frame_count == 0:
            if self.index[0] != 5:
                self.index[0] = (self.index[0] + 1)
class collision_box:
    def __init__(self, shape, coordinates, rad_or_width): ### for shape, enter "circle" if you want a circular collision box, line otherwise. Coordinates should be given with the vector class.
        self.circle = (shape == "circle")
        self.coordinates = coordinates ### for a circle, one vector pair of coordinates, for a line give a list of two vectors representing each end.
        if self.circle:
            self.radius = rad_or_width
        else:
            self.width = rad_or_width 
            self.vector = (coordinates[1] - coordinates[0]) ## tracks the length and direction of the wall
            self.normal = (self.vector.get_normalized()).rotate_anti() ## perpendicular vector to the wall
            self.point = (coordinates[0] + coordinates[1]) / 2 ## mid point of the wall
            self.width_vector = self.normal * self.width
            self.corners = [coordinates[0]-(0.5*self.width_vector), coordinates[0]+(0.5*self.width_vector),
             coordinates[1]-(0.5*self.width_vector), coordinates[1]+(0.5*self.width_vector)]

            
    def changeCoords(self, coordinates):
        self.coordinates = coordinates ### for a circle, one vector pair of coordinates, for a line give a list of two vectors representing each end.
      
        if not self.circle:
            self.vector = (coordinates[1] - coordinates[0]) ## tracks the length and direction of the wall
            self.normal = (self.vector.get_normalized()).rotate_anti() ## perpendicular vector to the wall
            self.point = (coordinates[0] + coordinates[1]) / 2 ## mid point of the wall
            self.width_vector = self.normal * self.width
            self.corners = [coordinates[0]-(0.5*self.width_vector), coordinates[0]+(0.5*self.width_vector),
             coordinates[1]-(0.5*self.width_vector), coordinates[1]+(0.5*self.width_vector)]    
    
    def collide(self, other):
        if self.circle:
            if other.circle:
                return ((self.coordinates - other.coordinates).length() <= self.radius + other.radius)
            else:
                wall_to_circle = self.coordinates - other.point

    ## project the vector from the midpoint to the ball onto the wall's vector - if the length is greater than half the wall then the ball should not interact with the wall other than through the corners because it is beyond the wall's domain
                if (wall_to_circle.get_proj(other.vector)).length() <= (other.vector.length() / 2):
                    ## find length of perpendicular projection and see if it is less than or equal to the width of the wall plus the radius of the ball to see if they are in collision
                    if ((wall_to_circle.get_proj(other.normal)).length() <= self.radius + other.width/2):
                        return True
                ## same premise as the previous if statement but taking the other two sides of the rectangle for measurement
                if ((wall_to_circle.get_proj(other.normal)).length() <= other.width/2 ):
                    if ((wall_to_circle.get_proj(other.vector)).length() <= self.radius + (other.vector).length()/2):
                        return True
                
                for corner in other.corners:
                    if (self.coordinates - corner).length() <= self.radius:
                        return True
                return False
                        
        else: ## collisions will only be happening between balls and other balls, or balls and rectangles in the game
            return other.collide(self) ## avoid repeating code, use the collision method for if self.circle
    

    def draw(self, canvas, colour = 'Green'):
        if self.circle:
            canvas.draw_circle(self.coordinates.get_p(), self.radius, 1, colour, colour)
        else:
            canvas.draw_line(self.coordinates[0].get_p(), self.coordinates[1].get_p(), self.width, colour)
class Hitbox(collision_box):
    def __init__(self, coordinates, radius, damage, knockback = 0): ### hitboxes are always circles, they also contain fields for the damage they inflict and the knockback 
        super().__init__("circle", coordinates, radius)
        self.damage = damage
        self.knockback = knockback
class Moveset:
    def __init__(self):
        self.down = False
        self.left = False
        self.right = False
        self.jump = False
        self.light = False
        self.heavy = False
        self.p2Down = False
        self.p2Left = False
        self.p2Right = False
        self.p2Jump = False
        self.p2Light = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['up']:
            self.jump = True
        if key == simplegui.KEY_MAP['down']:
            self.down = True
        if key == simplegui.KEY_MAP['left']:
            self.left = True
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        if key == simplegui.KEY_MAP['H']:
            self.light = True
        
        if key == simplegui.KEY_MAP['W']:
            self.p2Jump = True
        if key == simplegui.KEY_MAP['S']:
            self.p2Down = True
        if key == simplegui.KEY_MAP['A']:
            self.p2Left = True
        if key == simplegui.KEY_MAP['D']:
            self.p2Right = True
        if key == simplegui.KEY_MAP['space']:
            self.p2Light = True
 

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['up']:
            self.jump = False
        if key == simplegui.KEY_MAP['down']:
            self.down = False
        if key == simplegui.KEY_MAP['left']:
            self.left = False
        if key == simplegui.KEY_MAP['right']:
            self.right = False 
        if key == simplegui.KEY_MAP['H']:
            self.light = False
        
        if key == simplegui.KEY_MAP['W']:
            self.p2Jump = False
        if key == simplegui.KEY_MAP['S']:
            self.p2Down = False
        if key == simplegui.KEY_MAP['A']:
            self.p2Left = False
        if key == simplegui.KEY_MAP['D']:
            self.p2Right = False 
        if key == simplegui.KEY_MAP['space']:
            self.p2Light = False
        
        
        
        
        
moveset = Moveset()
class WallBox(collision_box):
    def __init__(self, coordinates, width, direction): ### wallbox will make a rectangular collision box and takes a list of vector coordinates as an argument. The direction indicates the vector that the wall should push in when there is a collision with it, to prevent clipping through walls and being pushed in the other direction, this vector needs to be calculated manually based on the direction of the wall, but the constructor will automatically normalize it.
        super().__init__("line", coordinates, width)
        self.direction = direction.get_normalized()
class PlatformBox(collision_box):
    def __init__(self, coordinates, length, width, semisolid): ### coordinates is just one vector, length is an integer which specifies how long the platform is because a platform can only be flat, width is the integer width of the floorbox, semisolid is a boolean whether you can drop through and jump through the platform
        super().__init__("line", [coordinates, coordinates+Vector(length, 0)], width)
        self.semisolid = semisolid
        self.floor_height = coordinates.y - width/2
class Spritesheet:
    
    ### get jumping and crouching sprites + mirrors, put them and their correct frame index in character along with the if statements
    def __init__(self, pURL, prows, pcolumns, numFrames, posX, posY, pframeRate, charHeight, charWidth, pFrameIndex):
        
        self.pURL = pURL
        self.rows = prows
        self.columns = pcolumns
        self.numFrames = numFrames
        self.posX = posX
        self.posY = posY
        self.frameRate = pframeRate
        self.charHeight = charHeight
        self.charWidth = charWidth
        self.orientation = "r"
        self.width = self.pURL.get_width()
        self.height = self.pURL.get_height()
        
        self._init_dimension()
        
        self.frame_index = pFrameIndex
        
    

    def _init_dimension(self):
        self.frame_width = self.width / self.columns
        self.frame_height = self.height / self.rows
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2
        
    def draw(self, canvas):
    
        if self.numFrames > 6 and self.frame_index == [6, 1]:
            self.frame_index = [0, 2]
        if self.numFrames > 6 and self.frame_index == [6, 2]:
            self.frame_index = [0, 3]
        
        if self.frame_index[0] == 0 and self.frame_index[1] < 2:
            orientation = "r"
        else:
            orientation = "l"            
            
        

        source_centre = (self.frame_width * self.frame_index[0] + self.frame_centre_x,self.frame_height * self.frame_index[1] + self.frame_centre_y)
        source_size = (self.frame_width, self.frame_height)
        dest_centre = (self.posX, self.posY)
        dest_size = (self.charWidth, self.charHeight)

        canvas.draw_image(self.pURL, source_centre, source_size, dest_centre, dest_size)
    
    def draw2(self, canvas, horizIndex, verticIndex, position): ### give position to draw as a vector, the indices tell you where in the sheet
        centre_x = horizIndex * self.frame_width + self.frame_centre_x
        centre_y = verticIndex * self.frame_height + self.frame_centre_y

        canvas.draw_image(self.pURL, (centre_x, centre_y), (self.frame_width, self.frame_height), position.get_p(), (self.charWidth, self.charHeight))
        
    def next_frame(self):
        self.frame_index[0] = (self.frame_index[0] + 1) % self.columns
        if self.frame_index[0] == 0:
            self.frame_index[1] = (self.frame_index[1] + 1) % self.rows
      
    def Done(self):
        if self.numFrames == (self.frame_index[1]*self.columns +(self.frame_index[0]+1)):
            return True
        return False
class Game1P:
    def __init__(self, character):
        self.character = character
        self.moveset = moveset
        self.clock = Clock(0)
        self.stage = stage
        self.floors = [PlatformBox(Vector(130, 310), 540, 20, False), PlatformBox(Vector(180, 220), 70, 3, True),
        PlatformBox(Vector(550, 220), 70, 3, True)]
        self.walls = [WallBox([Vector(135,500), Vector(135,320)], 10, Vector(1, 0)), WallBox([Vector(665,500), Vector(665,320)], 10, Vector(-1, 0))]
        self.score = 0
        self.AIList = []
        self.AIKillList = []
        self.frameParity = 0
    
    def randGhostPos(self):
        vector = Vector(random.randrange(0,800), random.randrange(0,500))
        while (vector - self.character.pos).length() < 100:
            vector = Vector(random.randrange(0,800), random.randrange(0,500))
        return vector
                    
        
    def timerFunc(self):
            self.AIList.append(AI(self.randGhostPos()))    
    
    def draw(self, canvas):
        canvas.draw_image(self.stage, (400,250), (800,500), (400,250), (800,500))
        self.frameParity = (self.frameParity + 1) % 2
        
        if self.frameParity == 0:
            self.update()
        
            for AI in self.AIList:
                AI.update(self.character.pos)
                for hitbox in AI.hitbox:
                    if hitbox.collide(self.character.hurt_box):
                        self.character.die()
                for hitbox in self.character.hitbox:
                    if hitbox.collide(AI.hurtbox):
                        self.AIKillList.append(AI)
            for AI in self.AIKillList:
                self.AIList.remove(AI)
                self.score += 10
            self.AIKillList.clear()
        
        for AI in self.AIList:
            AI.draw(canvas)
         
        self.character.draw(canvas)
        canvas.draw_text('Lives: ' + str(self.character.lives), (10,30), 30, 'Black')
        canvas.draw_text('Score: ' + str(self.score), (10,60), 30, 'Black')
        
        if (self.character.pos.x < 0 or self.character.pos.x > 800 or
        self.character.pos.y < 0 or self.character.pos.y > 500):
            self.character.die()
        
        
                    
        #for floor in self.floors:
         #   floor.draw(canvas)
        #for wall in self.walls:
         #   wall.draw(canvas)

    def update(self):
        self.character.update(GRAVITY, (self.floors + self.walls))
        if not (self.character.light or self.character.heavy):
            if self.moveset.jump:
                self.character.Jumping()

                if ((self.character.grounded)):
                    self.character.vel.add((Vector(0, -5)))
            

            if self.moveset.right == True:
                if self.character.grounded:
                    self.character.Running()
                    self.character.left = False
        
                self.character.vel.add(Vector(1, 0)) 

            if self.moveset.left == True:
                if self.character.grounded:
                    self.character.Running()
                    self.character.left = True

                self.character.vel.add(Vector(-1, 0))

            if self.moveset.down == True:
                self.character.Crouching()
            if self.moveset.light == True and self.character.charType == "Brawler":
                self.character.AttackingBrawlLight()
            if self.moveset.heavy == True and self.character.charType == "Brawler":
                self.character.AttackingBrawlHeavy
            if self.moveset.light == True and self.character.charType == "Sword":
                self.character.AttackingSwordLight()
            if self.moveset.heavy == True and self.character.charType == "Sword":
                self.character.AttackingSwordHeavy()
            
            if self.character.grounded and not (self.moveset.down or self.moveset.light or self.moveset.heavy
                    or self.moveset.jump or self.moveset.right or self.moveset.left):
                self.character.Idle()

class Game2P:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.moveset = moveset
        self.clock = Clock(0)
        self.stage = stage
        self.floors = [PlatformBox(Vector(130, 310), 540, 20, False), PlatformBox(Vector(180, 220), 70, 3, True),
        PlatformBox(Vector(550, 220), 70, 3, True)]
        self.walls = [WallBox([Vector(135,500), Vector(135,320)], 10, Vector(1, 0)), WallBox([Vector(665,500), Vector(665,320)], 10, Vector(-1, 0))] 
        self.frameParity = 0
    
    def draw(self, canvas):
        self.frameParity = (self.frameParity + 1) % 2
        
        if self.frameParity == 0:
            self.update()
            p1Hit = False
            p2Hit = False
            for hitbox in self.player1.hitbox:
                if hitbox.collide(self.player2.hurt_box):
                    p1Hit = True
                    self.player2.damage += 15
                    if self.player1.left:
                        self.player2.vel = (self.player2.damage / 100) * Vector(-40, -30)
                    else:
                        self.player2.vel = (self.player2.damage / 100) * Vector(40, -30)
            for hitbox in self.player2.hitbox:
                if hitbox.collide(self.player1.hurt_box):
                    p2Hit = True
                    self.player1.damage += 12
                    if self.player2.left:
                        self.player1.vel = (self.player1.damage / 100) * Vector(-30, -20)
                    else:
                        self.player1.vel = (self.player1.damage / 100) * Vector(30, -20)
        
            if p1Hit:
                self.player1.hitbox.clear()
            if p2Hit:
                self.player2.hitbox.clear()
        
        canvas.draw_image(self.stage, (400,250), (800,500), (400,250), (800,500)) 
        self.player1.draw(canvas)
        self.player2.draw(canvas)
        canvas.draw_text('P1 Lives: ' + str(self.player1.lives) + ', ' + str(self.player1.damage) + '%', (10,30), 30, 'Black')
        canvas.draw_text('P2 Lives: ' + str(self.player2.lives) + ', ' + str(self.player2.damage) + '%', (10,60), 30, 'Black')
        
        if (self.player1.pos.x < 0 or self.player1.pos.x > 800 or
        self.player1.pos.y < 0 or self.player1.pos.y > 500):
            self.player1.die()
        
        if (self.player2.pos.x < 0 or self.player2.pos.x > 800 or
        self.player2.pos.y < 0 or self.player2.pos.y > 500):
            self.player2.die()       
                    
        #for floor in self.floors:
         #   floor.draw(canvas)
        #for wall in self.walls:
         #   wall.draw(canvas)

    def update(self):
        self.player1.update(GRAVITY, (self.floors + self.walls))
        self.player2.update(GRAVITY, (self.floors + self.walls))
        if not (self.player1.light or self.player1.heavy):
            if self.moveset.jump:
                self.player1.Jumping()

                if ((self.player1.grounded)):
                    self.player1.vel.add((Vector(0, -5)))
            

            if self.moveset.right == True:
                if self.player1.grounded:
                    self.player1.Running()
                    self.player1.left = False
        
                self.player1.vel.add(Vector(1, 0)) 

            if self.moveset.left == True:
                if self.player1.grounded:
                    self.player1.Running()
                    self.player1.left = True

                self.player1.vel.add(Vector(-1, 0))

            if self.moveset.down == True:
                self.player1.Crouching()
            if self.moveset.light == True and self.player1.charType == "Brawler":
                self.player1.AttackingBrawlLight()
            if self.moveset.heavy == True and self.player1.charType == "Brawler":
                self.player1.AttackingBrawlHeavy
            if self.moveset.light == True and self.player1.charType == "Sword":
                self.player1.AttackingSwordLight()
            if self.moveset.heavy == True and self.player1.charType == "Sword":
                self.player1.AttackingSwordHeavy()
            
            if self.player1.grounded and not (self.moveset.down or self.moveset.light or self.moveset.heavy
                    or self.moveset.jump or self.moveset.right or self.moveset.left):
                self.player1.Idle()
        
        if not (self.player2.light or self.player2.heavy):
            if self.moveset.p2Jump:
                self.player2.Jumping()

                if ((self.player2.grounded)):
                    self.player2.vel.add((Vector(0, -5)))
            

            if self.moveset.p2Right:
                if self.player2.grounded:
                    self.player2.Running()
                    self.player2.left = False
        
                self.player2.vel.add(Vector(1, 0)) 

            if self.moveset.p2Left:
                if self.player2.grounded:
                    self.player2.Running()
                    self.player2.left = True

                self.player2.vel.add(Vector(-1, 0))

            if self.moveset.p2Down:
                self.player2.Crouching()
            if self.moveset.p2Light == True and self.player2.charType == "Brawler":
                self.player2.AttackingBrawlLight()
            if self.moveset.heavy == True and self.player2.charType == "Brawler":
                self.player2.AttackingBrawlHeavy
            if self.moveset.p2Light == True and self.player2.charType == "Sword":
                self.player2.AttackingSwordLight()
            if self.moveset.heavy == True and self.player2.charType == "Sword":
                self.player2.AttackingSwordHeavy()
            
            if self.player2.grounded and not (self.moveset.p2Down or self.moveset.p2Light or self.moveset.heavy
                    or self.moveset.p2Jump or self.moveset.p2Right or self.moveset.p2Left):
                self.player2.Idle()
        return

WIDTH = 800
HEIGHT = 500

class Menu:
    def __init__(self):
        self.game1P = Game1P(Character(Vector(WIDTH / 2, 0)))
        self.game2P = Game2P(Character(Vector(WIDTH / 4, 0)), SwordCharacter(Vector(3 * WIDTH / 4, 0)))
        self.high_score = 0
        self.in1P = False
        self.in2P = False
        self.menuNumber = 1
        self.menu1Image = titleScreen
    
    def draw(self, canvas):
        

        if self.in1P:
            if self.game1P.character.lives > 0:
                self.game1P.draw(canvas)
            else:
                self.in1P = False
                self.menuNumber = 1
                self.game1P.AIList.clear()
                timer.stop()
                self.game1P.character.lives = 3
                if self.game1P.score > self.high_score:
                    self.high_score = self.game1P.score
                self.game1P.score = 0
                
        elif self.in2P:
            if self.game2P.player1.lives > 0 and self.game2P.player2.lives > 0:
                self.game2P.draw(canvas)
            else:
                self.in2P = False
                self.menuNumber = 1
                self.game2P.player1.lives = 3
                self.game2P.player2.lives = 3
                
        elif self.menuNumber == 1:
            canvas.draw_image(self.menu1Image, (400,250), (800,500), (400,250), (800,500))
            canvas.draw_circle((150, 330), 65, 1, 'Black', '#ff461c')
            canvas.draw_text('Solo Mode', (90, 340), 27, 'Black')
            canvas.draw_text('High Score: ' + str(self.high_score), (65, 260), 27, 'Black')
            
            canvas.draw_circle((650, 330), 65, 1, 'Black', '#147aff')
            canvas.draw_text('2 Player', (600, 340), 30, 'Black')

        elif self.menuNumber == 2:
            frame.set_canvas_background('Black') #placeholder for an actual menu background
            canvas.draw_text('2 player battle!', (180, 100), 70, 'Red')
            canvas.draw_text('Player 1: Arrow keys to move. H to attack.', (130, 200), 36, 'Red')
            canvas.draw_text('Player 2: WASD to move. Space to attack.', (130, 250), 36, 'Red')
            
            canvas.draw_text('Goal: Make your opponent lose their lives before you lose yours.', (100, 350), 24, 'Red')
            canvas.draw_text('Click the mouse to start!', (130, 400), 36, 'Red')
            

        elif self.menuNumber == 3:
            frame.set_canvas_background('Black')
            canvas.draw_text('1 player mode!', (180, 100), 70, 'Red')
            canvas.draw_text('Use the arrow keys to move.', (130, 200), 36, 'Red')
            canvas.draw_text('Press H to attack.', (130, 250), 36, 'Red')
            
            canvas.draw_text('Goal: Survive while taking out as many ghosts as you can.', (100, 350), 24, 'Red')
            canvas.draw_text('Click the mouse to start!', (130, 400), 36, 'Red')
        
    
    def mouse_click(self, pos):
        if self.menuNumber == 1:
            if (Vector(pos[0] - 150, pos[1] - 330)).length() < 80:
                self.menuNumber = 3
                return
            elif (Vector(pos[0] - 650, pos[1] - 330)).length() < 80:
                self.menuNumber = 2
                return
            return
        elif self.menuNumber == 2:
            self.in2P = True
            self.game2P.player1.lives = 3
            self.game2P.player2.lives = 3
        elif self.menuNumber == 3: 
            self.in1P = True
            timer.start()
            self.game1P.character.lives = 3

m = Menu()


frame = simplegui.create_frame("The Game", WIDTH, HEIGHT)
frame.set_draw_handler(m.draw)
frame.set_mouseclick_handler(m.mouse_click)
frame.set_keyup_handler(moveset.keyUp)
frame.set_keydown_handler(moveset.keyDown)
timer = simplegui.create_timer(1500, m.game1P.timerFunc)
frame.start()


