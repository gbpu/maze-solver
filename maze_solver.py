#!/usr/bin/env python3

import time
import copy
import cv2 as cv

""" Solves mazes of http://www.mazegenerator.net/"""

### Get the maze image and found the center of all cells ###
start_time = time.time()

#FILENAME FORMAT:  "{X_GRID} BY {Y_GRID}... .png" 
#filename = "Maze_examples/200 by 200 orthogonal maze.png"
filename = input('Enter the path to file of the maze image: (e.g. "Maze_examples/20 by 20 orthogonal maze.png")\n')
mesh = input('Enter the mesh size separeted by space (e.g. "20 20"):\n')
maze = cv.imread(filename)

height, width = maze.shape[:2] #in pixels
#mesh_j, mesh_i = (int(filename.split()[0]), int(filename.split()[2]))
mesh_j, mesh_i = int(mesh.split()[0]), int(mesh.split()[1])

print(mesh_j, mesh_i)
cell_size = int(height/mesh_i) , int(width/mesh_j)
cell_center = (int(cell_size[0]/2), int(cell_size[1]/2))



class Cell:
      """defines the paths through the cells over the mesh """
     
      def __init__(self, index_i, index_j):
            global cell_size, height, width, maze, mesh_i, mesh_j
             
            self.i = index_i
            self.j = index_j
            self.height = height
            self.width = width
            self.cell_size_x, self.cell_size_y = (int(cell_size[0]), int(cell_size[1]))   
            (self.mesh_i, self.mesh_j) = (mesh_i, mesh_j)
            self.maze = maze
            self.tol =1               
         
      def to_coord(self):
            self.coord_x = int(self.j*self.cell_size_x + self.cell_size_x/2)
            self.coord_y = int(self.i*self.cell_size_y + self.cell_size_y/2)
            return (self.coord_x, self.coord_y)
      
      
     
      def left_pass(self):
        self.x, self.y = self.to_coord()
        self.left = int(self.x - (self.cell_size_x/2))
        for e in range(-self.tol,self.tol):
            try:
                if self.maze[self.y, self.left - e , 1] == 0:  #First Y and then X     
                    return False
            except:
                continue
        return True
        
      def right_pass(self):
         self.x, self.y = self.to_coord() 
         self.right = int(self.x + (self.cell_size_x/2))
         for e in range(-self.tol,self.tol):
            try:
                if self.maze[self.y, self.right + e, 1] == 0: #Y then X           
                    return False
            except:
                continue
         return True
    
      def top_pass(self):
         self.x, self.y = self.to_coord() 
         self.top = int(self.y - (self.cell_size_y/2))
         for e in range(-self.tol,self.tol):
             try:
                 if self.maze[ self.top-e, self.x, 1] == 0: #Y then X         
                    return False
             except:
                 continue   
         return True
             
      def bottom_pass(self):
         self.x, self.y = self.to_coord()         
         self.bot = int(self.y + (self.cell_size_y/2))
         for e in range(-self.tol,self.tol):
             try:
                 if self.maze[ self.bot + e, self.x, 1] == 0: #Y then X          
                     return False
             except:
                continue
         return True
     
      def go_to(self, start=None, end=None):
        self.start = start
        self.end = end
        
        Dest=[] #list of possibele destinations of each cell 
        if self.j!=0 and self.left_pass()==True:
            Dest.append((self.i, self.j-1))
        if self.j!=(self.mesh_j-1) and self.right_pass()==True:
            Dest.append((self.i, self.j+1))
        if self.i!=0 and self.top_pass()==True:
            Dest.append((self.i-1, self.j))
        if self.i!=(self.mesh_i-1) and self.bottom_pass()==True:
            Dest.append((self.i+1, self.j)) 
        return Dest


def Path():
    global start
    i = 0
    Nodes =[]
    Nodes_sol = []
    Destinations=[]
    Nodes=[]

    for i in range(mesh_i):
        line = []
        for j in range(mesh_j):
            dest =  Cell(i,j).go_to()
            line.append(dest)
            if i==0 and Cell(i,j).top_pass()==True:
                start = (i,j)
                if len(dest)>1:
                    Nodes.append((i,j))
            if i==(mesh_i-1) and Cell(i,j).bottom_pass()==True:
                end = (i,j)
                if len(dest)>1:
                    Nodes.append((i,j))
            if len(dest)>2 :
                Nodes.append((i,j))
        Destinations.append(line)

        
    #start = (0,250)
    #end= (mesh_i-1, 250)    
    Dest_sol =copy.deepcopy(Destinations)
    prev_step = start
    Block =[]    
    next_step=None
    branch = []
    Branches =[]    
    
    while True:
        if len(Destinations[prev_step[0]][prev_step[1]]) > 0:                
            next_step = Destinations[prev_step[0]][prev_step[1]][0]
            branch.append(prev_step)
           
            
            if len(Destinations[prev_step[0]][prev_step[1]]) > 1: 
                Nodes.append(prev_step)
                Nodes_sol.append(prev_step)
                poss_block_node = next_step
                Branches.append(branch)

                branch  = []
                branch.append(prev_step)                              

            Destinations[prev_step[0]][prev_step[1]].remove(next_step)   # block going 
            Destinations[next_step[0]][next_step[1]].remove(prev_step)   #block the return            

           
        elif (len(Destinations[next_step[0]][next_step[1]]))==0:                
            if next_step==end:
                print('Solved!')
                branch.append(end)
                Branches.append(branch)
                break
            next_step = Nodes[-1]
            block = poss_block_node
            Block.append(block)
            Nodes.remove(next_step)
            
            branch  = []
        prev_step = next_step
        i+=1
    print(f'{i} iterations')
    return Dest_sol,Branches , end, start
                  
            
def draw_path():
    Dest, Branches, end, start = Path()        
    
    #creates a clean list of points of the solution
    Br=[]
    for i in range(1,len(Branches)+1):
        Br.append(list(dict.fromkeys(Branches[-i])))    
    Tr =[Br[0]]
    
    for ele in (Br):
        if ele[-1] == Tr[0][0]:
            Tr.insert(0, ele)        
    Dots=[Tr[0][0]]
    
    for branch in Tr:
        for cell in branch:
            #cv.circle(maze, Cell(cell[0], cell[1]).to_coord() , 3, [0, 150, 255],-1)
            if cell != Dots[-1]:
                Dots.append(cell)  
    #dwaw the path lines 
    for i in range(len(Dots)-1):        
        coord1 = Cell(Dots[i][0], Dots[i][1]).to_coord()
        coord2 = Cell(Dots[i+1][0], Dots[i+1][1]).to_coord()
        
        cv.line(maze, coord1, coord2 , [255, 0, 0], 3)
    
    # draws a small datail of start and end 
    coord_start = Cell(Dots[0][0], Dots[0][1]).to_coord()
    coord_start = (coord_start[0], coord_start[1]- int(cell_size[1]/2))
    coord_end = Cell(Dots[-1][0], Dots[-1][1]).to_coord()
    coord_end = (coord_end[0], coord_end[1]+int(cell_size[1]/2))
    cv.line(maze, coord_start, Cell(Dots[0][0], Dots[0][1]).to_coord() , [255, 0, 0], 3)
    cv.line(maze, coord_end, Cell(Dots[-1][0], Dots[-1][1]).to_coord() , [255, 0, 0], 3)
    

    cv.imwrite(f'{mesh_i}_by_{mesh_j}_solved.png',maze)
    
    #elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed Time: {round(elapsed_time, 5)} secs')
    
    
draw_path()
        
        
