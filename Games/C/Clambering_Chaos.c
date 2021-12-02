#include <stdio.h>
#include <time.h>

enum COLORS
{
  BLUE = 1,
  GREEN = 2,
  RED = 4,
  YELLOW = 14,
  WHITE = 15
};

#include <termios.h>
#include <unistd.h>
#include <fcntl.h>

void c_gotoxy(int x, int y)
{
  printf("\x1b[%d;%dH", y, x);
  fflush(stdout);
}

int c_kbhit(void)
{
  struct termios oldt, newt;
  int ch;
  int oldf;

  tcgetattr(STDIN_FILENO, &oldt);
  newt = oldt;
  newt.c_lflag &= ~(ICANON | ECHO);
  tcsetattr(STDIN_FILENO, TCSANOW, &newt);
  oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
  fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);

  ch = getchar();
  
  //caution, here we got rid of the line that reset the getchar function to it's normal state 
  //(for having to press enter) the waiting at all is still reset back to normal.
  fcntl(STDIN_FILENO, F_SETFL, oldf);

  if (ch != EOF)
  {
    ungetc(ch, stdin);
    return 1;
  }

  return 0;
}




void c_clrscr()
{
  puts("\x1b[2J\x1b[1;1H");
  fflush(stdout);
}

void c_textcolor(int newcolor)
{
  //https://en.wikipedia.org/wiki/ANSI_escape_code

  const char * s = "\x1b[30m";

  switch (newcolor)
  {
  case BLUE:
    s = "\x1b[34m";
    break;

  case GREEN:
    s = "\x1b[32m";
    break;

  case RED:
    s = "\x1b[31;1m";
    break;

  case YELLOW:
    s = "\x1b[33;1m";
    break;

  case WHITE:
    s = "\x1b[37;1m";
    break;
  };

  printf("%s", s);
}

#include <errno.h>    
#include <unistd.h>
int msleep(long msec)
{
    struct timespec ts;
    int res;

    if (msec < 0)
    {
        errno = EINVAL;
        return -1;
    }

    ts.tv_sec = msec / 1000;
    ts.tv_nsec = (msec % 1000) * 1000000;

    do {
        res = nanosleep(&ts, &ts);
    } while (res && errno == EINTR);

    return res;
}
  


/*
this is where the code actually starts. the rest is so I can implement c_kbhit(). it seems like a lot, because it is.
*/

#define lenar(arr)     (sizeof(arr) / sizeof((arr)[0]))
void showBoard(int xs, int ys, char * board[ys][xs]){
    int a;
    for(a = 0; a<ys; a++){
        int b;
        for(b = 0; b<xs; b++){
            if(board[a][b] == "W"){
                c_textcolor(BLUE);
            }else if(board[a][b] == "*" || board[a][b] == "$" || board[a][b] == "#"){
                c_textcolor(GREEN);
            }else if(board[a][b] == "9" || board[a][b] == "8" || board[a][b] == "7" || board[a][b] == "6" || board[a][b] == "5" || board[a][b] == "4" || board[a][b] == "3" || board[a][b] == "2" || board[a][b] == "1" || board[a][b] == "0" || board[a][b] == ">" || board[a][b] == "<" || board[a][b] == "^" || board[a][b] == "+"){
                c_textcolor(RED);
            }else{
                c_textcolor(WHITE);
            }
            printf("%s", board[a][b]);
        }
        printf("\n");
    }
}

void reprintBoard(int xs, int ys, char * board[ys][xs], char * oldBoard[ys][xs]){
    int a;
    
    for(a = 0; a<ys; a++){
        int b;
        for(b = 0; b<xs; b++){
            if(board[a][b] != oldBoard[a][b]){
                if(board[a][b] == "W"){
                    c_textcolor(BLUE);
                }else if(board[a][b] == "*" || board[a][b] == "$" || board[a][b] == "#"){
                    c_textcolor(GREEN);
                }else if(board[a][b] == "9" || board[a][b] == "8" || board[a][b] == "7" || board[a][b] == "6" || board[a][b] == "5" || board[a][b] == "4" || board[a][b] == "3" || board[a][b] == "2" || board[a][b] == "1" || board[a][b] == "0" || board[a][b] == ">" || board[a][b] == "<" || board[a][b] == "^" || board[a][b] == "+"){
                    c_textcolor(RED);
                }else{
                    c_textcolor(WHITE);
                }
                c_gotoxy(b+1, a+2);
                printf("%s", board[a][b]);
                c_gotoxy(1, ys+2);
            }
        }
    }
}

#include <stdlib.h>
int randi(int min, int max){
    srand(clock());
    return (rand() %(max - min + 1)) + min;
}

int main() {
    while(1){
    printf("\x1b[?25l");
    int SIZEY = 20;
    int SIZEX = 50;
    int position[2];
    position[0] = SIZEX/2;
    position[1] = SIZEY/2;
    int a;
    char * board[SIZEY][SIZEX];
    char * oldBoard[SIZEY][SIZEX];
    for(a = 0; a<SIZEY-1; a++){
        int b;
        for(b = 0; b<SIZEX-1; b++){
            oldBoard[a][b] = board[a][b];
        }
    }
    //Start of directions in ascii
    int up = 119;
    int right = 100;
    int down = 115;
    int left = 97;
    //End of directions in ascii
    
    //Start of board making
    for(a = 0; a<SIZEY; a++){
        int b;
        for(b = 0; b<SIZEX; b++){
            board[a][b] = " ";
        }
    }
    printf("%s\n", board[0][2]);
    for(a = 0; a<SIZEX; a++){
        board[0][a] = "W";
        board[SIZEY-1][a] = "W";
    }
    for(a = 0; a<SIZEY; a++){
        board[a][0] = "W";
        board[a][SIZEX-1] = "W";
    }
    //End of board making
    c_clrscr();
    showBoard(SIZEX, SIZEY, board);
    int key = 0;
    int numBullets;
    
    //order is [[xpos, ypos, turns left]...] 'turns left' is the countdown before it leaves the edges
    //it's not fair to have the bullets come out of nowhere without the player seeing them first
    int rightBullets[SIZEY][3];
    int leftBullets[SIZEY][3];
    int upBullets[SIZEX][3];
    
    for(a = 0; a<SIZEY; a++){
        rightBullets[a][2] = -1;
        leftBullets[a][2] = -1;
        upBullets[a][2] = -1;
    }
    
    //format is [[xpos, ypos, turns left]...] 
    int rightSliceBullets[SIZEY][3];
    int leftSliceBullets[SIZEY][3];
    int upSliceBullets[SIZEX][3];
    
    for(a = 0; a<SIZEY; a++){
        rightSliceBullets[a][2] = -1;
        leftSliceBullets[a][2] = -1;
        upSliceBullets[a][2] = -1;
    }
    
    //format is [xpos, ypos] money signs just give you 1000 score
    int moneySign[2];
    moneySign[1] = randi(1, SIZEY-2);
    moneySign[0] = randi(1, SIZEX-2);
    
    //chooses how fast the board updates 
    //the higher the speed the faster the bullets the faster the response time of the player
    int SPEED = 100;
    int score = 0;
    
    //format is [xpos, ypos, turns left], be careful of bombs. they will kill the player
    int bomb[2];
    bomb[2] = -1;
    
    int numBlips = 0;
    
    int level = 1;
    int lives = 3;
    
    int highScore;
    FILE *fyle;
    if ((fyle = fopen("highScore.txt","r")) == NULL){
        fyle = fopen("highScore.txt","w");
        highScore = 10;
        printf("The high score file had to be created before the game could work. please try again.");
        fprintf(fyle,"%d",highScore);
        return 0;
        fclose(fyle);
    }else{
        fyle = fopen("highScore.txt","r");
        fscanf(fyle,"%d", &highScore);
    }
    
    //game
    while(1){
        msleep(SPEED);
        //Start of updating board
        //player
        board[position[1]][position[0]] = "*";
        //bullets
        for(a = 0; a<SIZEY; a++){
            if(leftBullets[a][2] != -1){
                //left bullets
                if(leftBullets[a][2] == 0){
                    board[leftBullets[a][1]][leftBullets[a][0]] = "<";
                }else if(leftBullets[a][2] == 1){
                    board[leftBullets[a][1]][leftBullets[a][0]] = "1";
                }else if(leftBullets[a][2] == 2){
                    board[leftBullets[a][1]][leftBullets[a][0]] = "2";
                }else if(leftBullets[a][2] == 3){
                    board[leftBullets[a][1]][leftBullets[a][0]] = "3";
                }else if(leftBullets[a][2] == 4){
                    board[leftBullets[a][1]][leftBullets[a][0]] = "4";
                }else if(leftBullets[a][2] == 5){
                    board[leftBullets[a][1]][leftBullets[a][0]] = "5";
                }else if(leftBullets[a][2] == 6){
                    board[leftBullets[a][1]][leftBullets[a][0]] = "6";
                }else if(leftBullets[a][2] == 7){
                    board[leftBullets[a][1]][leftBullets[a][0]] = "7";
                }else if(leftBullets[a][2] == 8){
                    board[leftBullets[a][1]][leftBullets[a][0]] = "8";
                }else if(leftBullets[a][2] == 9){
                    board[leftBullets[a][1]][leftBullets[a][0]] = "9";
                }
            }
            if(rightBullets[a][2] != -1){
                //right bullets
                if(rightBullets[a][2] == 0){
                    board[rightBullets[a][1]][rightBullets[a][0]] = ">";
                }else if(rightBullets[a][2] == 1){
                    board[rightBullets[a][1]][rightBullets[a][0]] = "1";
                }else if(rightBullets[a][2] == 2){
                    board[rightBullets[a][1]][rightBullets[a][0]] = "2";
                }else if(rightBullets[a][2] == 3){
                    board[rightBullets[a][1]][rightBullets[a][0]] = "3";
                }else if(rightBullets[a][2] == 4){
                    board[rightBullets[a][1]][rightBullets[a][0]] = "4";
                }else if(rightBullets[a][2] == 5){
                    board[rightBullets[a][1]][rightBullets[a][0]] = "5";
                }else if(rightBullets[a][2] == 6){
                    board[rightBullets[a][1]][rightBullets[a][0]] = "6";
                }else if(rightBullets[a][2] == 7){
                    board[rightBullets[a][1]][rightBullets[a][0]] = "7";
                }else if(rightBullets[a][2] == 8){
                    board[rightBullets[a][1]][rightBullets[a][0]] = "8";
                }else if(rightBullets[a][2] == 9){
                    board[rightBullets[a][1]][rightBullets[a][0]] = "9";
                }
            }
            if(upBullets[a][2] != -1){
                //up bullets
                if(upBullets[a][2] == 0){
                    board[upBullets[a][1]][upBullets[a][0]] = "^";
                }else if(upBullets[a][2] == 1){
                    board[upBullets[a][1]][upBullets[a][0]] = "1";
                }else if(upBullets[a][2] == 2){
                    board[upBullets[a][1]][upBullets[a][0]] = "2";
                }else if(upBullets[a][2] == 3){
                    board[upBullets[a][1]][upBullets[a][0]] = "3";
                }else if(upBullets[a][2] == 4){
                    board[upBullets[a][1]][upBullets[a][0]] = "4";
                }else if(upBullets[a][2] == 5){
                    board[upBullets[a][1]][upBullets[a][0]] = "5";
                }else if(upBullets[a][2] == 6){
                    board[upBullets[a][1]][upBullets[a][0]] = "6";
                }else if(upBullets[a][2] == 7){
                    board[upBullets[a][1]][upBullets[a][0]] = "7";
                }else if(upBullets[a][2] == 8){
                    board[upBullets[a][1]][upBullets[a][0]] = "8";
                }else if(upBullets[a][2] == 9){
                    board[upBullets[a][1]][upBullets[a][0]] = "9";
                }
            }
        }
        
        //slices
        for(a = 0; a<SIZEY; a++){
            if(leftSliceBullets[a][2] != -1){
                //left 
                if(leftSliceBullets[a][2] == 0){
                    board[leftSliceBullets[a][1]][leftSliceBullets[a][0]] = "<";
                }else if(leftSliceBullets[a][2] == 1){
                    board[leftSliceBullets[a][1]][leftSliceBullets[a][0]] = "1";
                }else if(leftSliceBullets[a][2] == 2){
                    board[leftSliceBullets[a][1]][leftSliceBullets[a][0]] = "2";
                }else if(leftSliceBullets[a][2] == 3){
                    board[leftSliceBullets[a][1]][leftSliceBullets[a][0]] = "3";
                }else if(leftSliceBullets[a][2] == 4){
                    board[leftSliceBullets[a][1]][leftSliceBullets[a][0]] = "4";
                }else if(leftSliceBullets[a][2] == 5){
                    board[leftSliceBullets[a][1]][leftSliceBullets[a][0]] = "5";
                }else if(leftSliceBullets[a][2] == 6){
                    board[leftSliceBullets[a][1]][leftSliceBullets[a][0]] = "6";
                }else if(leftSliceBullets[a][2] == 7){
                    board[leftSliceBullets[a][1]][leftSliceBullets[a][0]] = "7";
                }else if(leftSliceBullets[a][2] == 8){
                    board[leftSliceBullets[a][1]][leftSliceBullets[a][0]] = "8";
                }else if(leftSliceBullets[a][2] == 9){
                    board[leftSliceBullets[a][1]][leftSliceBullets[a][0]] = "9";
                }
            }
            if(rightSliceBullets[a][2] != -1){
                //right 
                if(rightSliceBullets[a][2] == 0){
                    board[rightSliceBullets[a][1]][rightSliceBullets[a][0]] = ">";
                }else if(rightSliceBullets[a][2] == 1){
                    board[rightSliceBullets[a][1]][rightSliceBullets[a][0]] = "1";
                }else if(rightSliceBullets[a][2] == 2){
                    board[rightSliceBullets[a][1]][rightSliceBullets[a][0]] = "2";
                }else if(rightSliceBullets[a][2] == 3){
                    board[rightSliceBullets[a][1]][rightSliceBullets[a][0]] = "3";
                }else if(rightSliceBullets[a][2] == 4){
                    board[rightSliceBullets[a][1]][rightSliceBullets[a][0]] = "4";
                }else if(rightSliceBullets[a][2] == 5){
                    board[rightSliceBullets[a][1]][rightSliceBullets[a][0]] = "5";
                }else if(rightSliceBullets[a][2] == 6){
                    board[rightSliceBullets[a][1]][rightSliceBullets[a][0]] = "6";
                }else if(rightSliceBullets[a][2] == 7){
                    board[rightSliceBullets[a][1]][rightSliceBullets[a][0]] = "7";
                }else if(rightSliceBullets[a][2] == 8){
                    board[rightSliceBullets[a][1]][rightSliceBullets[a][0]] = "8";
                }else if(rightSliceBullets[a][2] == 9){
                    board[rightSliceBullets[a][1]][rightSliceBullets[a][0]] = "9";
                }
            }
            if(upSliceBullets[a][2] != -1){
                //up 
                if(upSliceBullets[a][2] == 0){
                    board[upSliceBullets[a][1]][upSliceBullets[a][0]] = "^";
                }else if(upSliceBullets[a][2] == 1){
                    board[upSliceBullets[a][1]][upSliceBullets[a][0]] = "1";
                }else if(upSliceBullets[a][2] == 2){
                    board[upSliceBullets[a][1]][upSliceBullets[a][0]] = "2";
                }else if(upSliceBullets[a][2] == 3){
                    board[upSliceBullets[a][1]][upSliceBullets[a][0]] = "3";
                }else if(upSliceBullets[a][2] == 4){
                    board[upSliceBullets[a][1]][upSliceBullets[a][0]] = "4";
                }else if(upSliceBullets[a][2] == 5){
                    board[upSliceBullets[a][1]][upSliceBullets[a][0]] = "5";
                }else if(upSliceBullets[a][2] == 6){
                    board[upSliceBullets[a][1]][upSliceBullets[a][0]] = "6";
                }else if(upSliceBullets[a][2] == 7){
                    board[upSliceBullets[a][1]][upSliceBullets[a][0]] = "7";
                }else if(upSliceBullets[a][2] == 8){
                    board[upSliceBullets[a][1]][upSliceBullets[a][0]] = "8";
                }else if(upSliceBullets[a][2] == 9){
                    board[upSliceBullets[a][1]][upSliceBullets[a][0]] = "9";
                }
            }
        }
        //money sign
        board[moneySign[1]][moneySign[0]] = "$";
        
        //bomb
        if(bomb[2] != -1){
            if(bomb[2] == 1){
                board[bomb[1]][bomb[0]] = "1";
            }else if(bomb[2] == 2){
                board[bomb[1]][bomb[0]] = "2";
            }else if(bomb[2] == 3){
                board[bomb[1]][bomb[0]] = "3";
            }else if(bomb[2] == 4){
                board[bomb[1]][bomb[0]] = "4";
            }else if(bomb[2] == 5){
                board[bomb[1]][bomb[0]] = "5";
            }else if(bomb[2] == 6){
                board[bomb[1]][bomb[0]] = "6";
            }else if(bomb[2] == 7){
                board[bomb[1]][bomb[0]] = "7";
            }else if(bomb[2] == 8){
                board[bomb[1]][bomb[0]] = "8";
            }else if(bomb[2] == 9){
                board[bomb[1]][bomb[0]] = "9";
            }else{
                board[bomb[1]][bomb[0]] = "+";
                board[bomb[1]+1][bomb[0]] = "+";
                board[bomb[1]][bomb[0]+1] = "+";
                board[bomb[1]+1][bomb[0]+1] = "+";
                board[bomb[1]-1][bomb[0]] = "+";
                board[bomb[1]][bomb[0]-1] = "+";
                board[bomb[1]-1][bomb[0]-1] = "+";
                board[bomb[1]+1][bomb[0]-1] = "+";
                board[bomb[1]-1][bomb[0]+1] = "+";
                bomb[2] = -1;
            }
        }
        
        
        
        //End of updating board
        
        //checks if the player died
        c_textcolor(WHITE);
        if(board[position[1]][position[0]] != " " && board[position[1]][position[0]] != "*" && board[position[1]][position[0]] != "$" && board[position[1]][position[0]] != "9" && board[position[1]][position[0]] != "8" && board[position[1]][position[0]] != "7" && board[position[1]][position[0]] != "6" && board[position[1]][position[0]] != "5" && board[position[1]][position[0]] != "4" && board[position[1]][position[0]] != "3" && board[position[1]][position[0]] != "2" && board[position[1]][position[0]] != "1" && board[position[1]][position[0]] != "0"){
            c_clrscr();
            lives--;
            msleep(500);
            printf("You died and have %i lives left\nPress any key to continue", lives);
            for(a = 0; a<SIZEY; a++){
                int b;
                for(b = 0; b<SIZEX; b++){
                    board[a][b] = " ";
                }
            }
            printf("%s\n", board[0][2]);
            for(a = 0; a<SIZEX; a++){
                board[0][a] = "W";
                board[SIZEY-1][a] = "W";
            }
            for(a = 0; a<SIZEY; a++){
                board[a][0] = "W";
                board[a][SIZEX-1] = "W";
            }
            for(a = 0; a<SIZEY; a++){
                rightBullets[a][2] = -1;
                leftBullets[a][2] = -1;
                upBullets[a][2] = -1;
            }
            for(a = 0; a<SIZEY; a++){
                rightSliceBullets[a][2] = -1;
                leftSliceBullets[a][2] = -1;
                upSliceBullets[a][2] = -1;
            }
            score+=10;
            numBlips = 0;
            getchar();
            msleep(500);
            oldBoard[moneySign[1]][moneySign[0]] = " ";
            c_clrscr();
            showBoard(SIZEX, SIZEY, board);
        }
        if(lives<=0){
            break;
        }
        
        //checks if the player picked up a money sign
        if(board[position[1]][position[0]] == "$"){
            board[position[1]][position[0]] = " ";
            moneySign[0] = randi(1, SIZEX-2);
            moneySign[1] = randi(1, SIZEY-2);
            score += 1000;
        }
        score+=1;
        //prints your stats at the bottom of the screen
        c_textcolor(YELLOW);
        printf("Score: %i", score);
        c_textcolor(WHITE);
        printf(",");
        printf("\e[35m");
        printf("Lives: %i", lives);
        c_textcolor(WHITE);
        printf(",");
        c_textcolor(GREEN);
        printf("High Score: %i\n", highScore);
        
        
        reprintBoard(SIZEX, SIZEY, board, oldBoard);
        for(a = 0; a<SIZEY-1; a++){
            int b;
            for(b = 0; b<SIZEX-1; b++){
                oldBoard[a][b] = board[a][b];
            }
        }
        //Start of movements
        if(c_kbhit()){
            key = getchar();
            if(key == 27){
                break;
            }else if(key == up){
                if(board[position[1]-1][position[0]] != "W"){
                    board[position[1]][position[0]] = " ";
                    position[1]--;
                }
            }else if(key == right){
                if(board[position[1]][position[0]+1] != "W"){
                    board[position[1]][position[0]] = " ";
                    position[0]++;
                }
            }else if(key == down){
                if(board[position[1]+1][position[0]] != "W"){
                    board[position[1]][position[0]] = " ";
                    position[1]++;
                }
            }else if(key == left){
                if(board[position[1]][position[0]-1] != "W"){
                    board[position[1]][position[0]] = " ";
                    position[0]--;
                }
            }
        }
        //End of movements
        
        //Start of bullet's movements
        //left bullets
        for(a = 0; a<SIZEY; a++){
            if(leftBullets[a][2] != -1){
                if(leftBullets[a][2] == 0){
                    //if(leftBullets[a][0] == 0){
                    if(board[leftBullets[a][1]][leftBullets[a][0]-1] != " " && board[leftBullets[a][1]][leftBullets[a][0]-1] != "*" && board[leftBullets[a][1]][leftBullets[a][0]-1] != "$" && board[leftBullets[a][1]][leftBullets[a][0]-1] != "+"){
                        board[leftBullets[a][1]][leftBullets[a][0]] = "W";
                        leftBullets[a][2] = -1;
                    }else if(leftBullets[a][0] + 1 == SIZEX){
                        board[leftBullets[a][1]][leftBullets[a][0]] = "W";
                        leftBullets[a][0]--;
                    }else{
                        board[leftBullets[a][1]][leftBullets[a][0]] = " ";
                        leftBullets[a][0]--;
                    }
                }else{
                    leftBullets[a][2]--;
                }
            }
        }
        //right bullets
        for(a = 0; a<SIZEY; a++){
            if(rightBullets[a][2] != -1){
                if(rightBullets[a][2] == 0){
                    if(rightBullets[a][0] == 0){
                        board[rightBullets[a][1]][rightBullets[a][0]] = "W";
                        rightBullets[a][0]++;
                    //}else if(rightBullets[a][0] + 1 == SIZEX){
                    }else if(board[rightBullets[a][1]][rightBullets[a][0]+1] != " " && board[rightBullets[a][1]][rightBullets[a][0]+1] != "*" && board[rightBullets[a][1]][rightBullets[a][0]+1] != "$" && board[rightBullets[a][1]][rightBullets[a][0]+1] != "+"){
                        board[rightBullets[a][1]][rightBullets[a][0]] = "W";
                        rightBullets[a][2] = -1;
                    }else{
                        board[rightBullets[a][1]][rightBullets[a][0]] = " ";
                        rightBullets[a][0]++;
                    }
                }else{
                    rightBullets[a][2]--;
                }
            }
        }
        //up bullets
        for(a = 0; a<SIZEY; a++){
            if(upBullets[a][2] != -1){
                if(upBullets[a][2] == 0){
                    if(upBullets[a][1] == SIZEY-1){
                        board[upBullets[a][1]][upBullets[a][0]] = "W";
                        upBullets[a][1]--;
                    //}else if(upBullets[a][1] == 0){
                    }else if(board[upBullets[a][1]-1][upBullets[a][0]] != " " && board[upBullets[a][1]-1][upBullets[a][0]] != "*" && board[upBullets[a][1]-1][upBullets[a][0]] != "$" && board[upBullets[a][1]-1][upBullets[a][0]] != "+"){
                        board[upBullets[a][1]][upBullets[a][0]] = "W";
                        upBullets[a][2] = -1;
                    }else{
                        board[upBullets[a][1]][upBullets[a][0]] = " ";
                        upBullets[a][1]--;
                    }
                }else{
                    upBullets[a][2]--;
                }
            }
        }
        
        //getting the number of activated bullets
        numBullets = 0;
        for(a = 0; a<SIZEY; a++){
            if(leftBullets[a][2] != -1){
                numBullets++;
            }
            if(rightBullets[a][2] != -1){
                numBullets++;
            }
        }
        
        //every five seconds another bullet is allowed to be added. 
        //this add those bullets
        int randnum = randi(0, 2);
        if((clock()/1000)/5 > numBullets){
            if(randnum == 0){
                //lefts
                for(a = 0; a<SIZEY; a++){
                    if(leftBullets[a][2] == -1){
                        leftBullets[a][0] = SIZEX-1;
                        leftBullets[a][1] = randi(1, SIZEY-2);
                        leftBullets[a][2] = 9;
                        break;
                    }
                }
            }else if(randnum == 1){
                //rights
                for(a = 0; a<SIZEY; a++){
                    if(rightBullets[a][2] == -1){
                        rightBullets[a][0] = 0;
                        rightBullets[a][1] = randi(1, SIZEY-2);
                        rightBullets[a][2] = 9;
                        break;
                    }
                }
            }else if(randnum == 2){
                //ups
                for(a = 0; a<SIZEX; a++){
                    if(upBullets[a][2] == -1){
                        upBullets[a][1] = SIZEY-1;
                        upBullets[a][0] = randi(1, SIZEX-2);
                        upBullets[a][2] = 9;
                        break;
                    }
                }
            }
        }
        //End of bullet's movements
        
        //Start of slice bullet's movements
        //left
        for(a = 0; a<SIZEY; a++){
            if(leftSliceBullets[a][2] != -1){
                if(leftSliceBullets[a][2] == 0){
                    //if(leftBullets[a][0] == 0){
                    if(board[leftSliceBullets[a][1]][leftSliceBullets[a][0]-1] != " " && board[leftSliceBullets[a][1]][leftSliceBullets[a][0]-1] != "*" && board[leftSliceBullets[a][1]][leftSliceBullets[a][0]-1] != "$" && board[leftSliceBullets[a][1]][leftSliceBullets[a][0]-1] != "+"){
                        board[leftSliceBullets[a][1]][leftSliceBullets[a][0]] = "W";
                        int b;
                        leftSliceBullets[a][2] = -1;
                    }else if(leftSliceBullets[a][0] + 1 == SIZEX){
                        board[leftSliceBullets[a][1]][leftSliceBullets[a][0]] = "W";
                        leftSliceBullets[a][0]--;
                    }else{
                        board[leftSliceBullets[a][1]][leftSliceBullets[a][0]] = "+";
                        leftSliceBullets[a][0]--;
                    }
                }else{
                    leftSliceBullets[a][2]--;
                }
            }
        }
        //right 
        for(a = 0; a<SIZEY; a++){
            if(rightSliceBullets[a][2] != -1){
                if(rightSliceBullets[a][2] == 0){
                    if(rightSliceBullets[a][0] == 0){
                        board[rightSliceBullets[a][1]][rightSliceBullets[a][0]] = "W";
                        rightSliceBullets[a][0]++;
                    //}else if(rightBullets[a][0] + 1 == SIZEX){
                    }else if(board[rightSliceBullets[a][1]][rightSliceBullets[a][0]+1] != " " && board[rightSliceBullets[a][1]][rightSliceBullets[a][0]+1] != "*" && board[rightSliceBullets[a][1]][rightSliceBullets[a][0]+1] != "$" && board[rightSliceBullets[a][1]][rightSliceBullets[a][0]+1] != "+"){
                        board[rightSliceBullets[a][1]][rightSliceBullets[a][0]] = "W";
                        int b;
                        rightSliceBullets[a][2] = -1;
                    }else{
                        board[rightSliceBullets[a][1]][rightSliceBullets[a][0]] = "+";
                        rightSliceBullets[a][0]++;
                    }
                }else{
                    rightSliceBullets[a][2]--;
                }
            }
        }
        //up 
        for(a = 0; a<SIZEY; a++){
            if(upSliceBullets[a][2] != -1){
                if(upSliceBullets[a][2] == 0){
                    if(upSliceBullets[a][1] == SIZEY-1){
                        board[upSliceBullets[a][1]][upSliceBullets[a][0]] = "W";
                        upSliceBullets[a][1]--;
                    //}else if(upBullets[a][1] == 0){
                    }else if(board[upSliceBullets[a][1]-1][upSliceBullets[a][0]] != " " && board[upSliceBullets[a][1]-1][upSliceBullets[a][0]] != "*" && board[upSliceBullets[a][1]-1][upSliceBullets[a][0]] != "$" && board[upSliceBullets[a][1]-1][upSliceBullets[a][0]] != "+"){
                        board[upSliceBullets[a][1]][upSliceBullets[a][0]] = "W";
                        int b;
                        upSliceBullets[a][2] = -1;
                    }else{
                        board[upSliceBullets[a][1]][upSliceBullets[a][0]] = "+";
                        upSliceBullets[a][1]--;
                    }
                }else{
                    upSliceBullets[a][2]--;
                }
            }
        }
        
        //adds a slice bullet at random times
        randnum = randi(0, 2);
        if((clock()%20) == 0){
            if(randnum == 0){
                //lefts
                for(a = 0; a<SIZEY; a++){
                    if(leftSliceBullets[a][2] == -1){
                        leftSliceBullets[a][0] = SIZEX-1;
                        leftSliceBullets[a][1] = randi(1, SIZEY-2);
                        leftSliceBullets[a][2] = 9;
                        break;
                    }
                }
            }else if(randnum == 1){
                //rights
                for(a = 0; a<SIZEY; a++){
                    if(rightSliceBullets[a][2] == -1){
                        rightSliceBullets[a][0] = 0;
                        rightSliceBullets[a][1] = randi(1, SIZEY-2);
                        rightSliceBullets[a][2] = 9;
                        break;
                    }
                }
            }else if(randnum == 2){
                //ups
                for(a = 0; a<SIZEX; a++){
                    if(upSliceBullets[a][2] == -1){
                        upSliceBullets[a][1] = SIZEY-1;
                        upSliceBullets[a][0] = randi(1, SIZEX-2);
                        upSliceBullets[a][2] = 9;
                        break;
                    }
                }
            }
        }
        //End of slice bullets movements
        
        
        //clears board at random times
        if(clock()%150==0){
            numBlips = 1;
        }
        
        if(numBlips>0){
            if(numBlips%2 == 0){
                c_textcolor(RED);
            }else{
                c_textcolor(GREEN);
            }
            c_gotoxy(0, SIZEY+2);
            c_clrscr();
            showBoard(SIZEX, SIZEY, board);
            oldBoard[position[1]][position[0]] = " ";
            numBlips++;
        }
        
        if(numBlips>=5){
            for(a = 0; a<SIZEY; a++){
                int b;
                for(b = 0; b<SIZEX; b++){
                    board[a][b] = " ";
                }
            }
            printf("%s\n", board[0][2]);
            for(a = 0; a<SIZEX; a++){
                board[0][a] = "W";
                board[SIZEY-1][a] = "W";
            }
            for(a = 0; a<SIZEY; a++){
                board[a][0] = "W";
                board[a][SIZEX-1] = "W";
            }
            score+=10;
            oldBoard[moneySign[1]][moneySign[0]] = " ";
            numBlips = 0;
            c_clrscr();
            showBoard(SIZEX, SIZEY, board);
            oldBoard[position[1]][position[0]] = " ";
        }
        
        
        //bombs movements
        if(bomb[2] == -1){
            bomb[1] = randi(2, SIZEY-3);
            bomb[0] = randi(2, SIZEX-3);
            bomb[2] = 9;
        }else{
            bomb[2]--;
        }
        
        //checks if the player died
        c_textcolor(WHITE);
        if(board[position[1]][position[0]] != " " && board[position[1]][position[0]] != "*" && board[position[1]][position[0]] != "$" && board[position[1]][position[0]] != "9" && board[position[1]][position[0]] != "8" && board[position[1]][position[0]] != "7" && board[position[1]][position[0]] != "6" && board[position[1]][position[0]] != "5" && board[position[1]][position[0]] != "4" && board[position[1]][position[0]] != "3" && board[position[1]][position[0]] != "2" && board[position[1]][position[0]] != "1" && board[position[1]][position[0]] != "0"){
            c_clrscr();
            lives--;
            msleep(500);
            printf("You died and have %i lives left\nPress any key to continue", lives);
            if(score>highScore){
                highScore = score;
                fyle = fopen("highScore.txt","w");
                fprintf(fyle,"%d", highScore);
                fclose(fyle);
            }
            for(a = 0; a<SIZEY; a++){
                int b;
                for(b = 0; b<SIZEX; b++){
                    board[a][b] = " ";
                }
            }
            printf("%s\n", board[0][2]);
            for(a = 0; a<SIZEX; a++){
                board[0][a] = "W";
                board[SIZEY-1][a] = "W";
            }
            for(a = 0; a<SIZEY; a++){
                board[a][0] = "W";
                board[a][SIZEX-1] = "W";
            }
            for(a = 0; a<SIZEY; a++){
                rightBullets[a][2] = -1;
                leftBullets[a][2] = -1;
                upBullets[a][2] = -1;
            }
            for(a = 0; a<SIZEY; a++){
                rightSliceBullets[a][2] = -1;
                leftSliceBullets[a][2] = -1;
                upSliceBullets[a][2] = -1;
            }
            score+=10;
            numBlips = 0;
            getchar();
            msleep(500);
            oldBoard[moneySign[1]][moneySign[0]] = " ";
            c_clrscr();
            showBoard(SIZEX, SIZEY, board);
        }
        if(score>10000*level){
            SPEED--;
            level++;
            lives+=3;
            c_clrscr();
            printf("You just leveled up...\n");
            if(level==100){
                printf("You are crazy! You beat the game! The levels from here on out are all the same. Keep going for the score, you got this!\n");
                printf("Press any keys twice to continue ");
            }
            msleep(500);
            printf("Now get ready for level %i\n", level);
            msleep(500);
            printf("Press any key to continue");
            if(score>highScore){
                highScore = score;
                fyle = fopen("highScore.txt","w");
                fprintf(fyle,"%d", highScore);
                fclose(fyle);
            }
            for(a = 0; a<SIZEY; a++){
                int b;
                for(b = 0; b<SIZEX; b++){
                    board[a][b] = " ";
                }
            }
            printf("%s\n", board[0][2]);
            for(a = 0; a<SIZEX; a++){
                board[0][a] = "W";
                board[SIZEY-1][a] = "W";
            }
            for(a = 0; a<SIZEY; a++){
                board[a][0] = "W";
                board[a][SIZEX-1] = "W";
            }
            for(a = 0; a<SIZEY; a++){
                rightBullets[a][2] = -1;
                leftBullets[a][2] = -1;
                upBullets[a][2] = -1;
            }
            for(a = 0; a<SIZEY; a++){
                rightSliceBullets[a][2] = -1;
                leftSliceBullets[a][2] = -1;
                upSliceBullets[a][2] = -1;
            }
            getchar();
            oldBoard[position[1]][position[0]] = " ";
            oldBoard[moneySign[1]][moneySign[0]] = " ";
            c_clrscr();
            showBoard(SIZEX, SIZEY, board);
        }
    }
    c_clrscr();
    c_textcolor(YELLOW);
    if(score>highScore){
        highScore = score;
        printf("You got a new high score of %i! You are amazing!", highScore);
        fyle = fopen("highScore.txt","w");
        fprintf(fyle,"%d", highScore);
        fclose(fyle);
    }else{
        printf("Nice game! You scored %i points", score);
    }
    printf("\nYou were on level %i", level);
    printf("\n\nWould you like to continue? ");
    sleep(1);
    int tobreak = 0;
    while(1){
        char yn = getchar();
        if(yn == 121){
            tobreak = 0;
            break;
        }else if(yn == 110){
            tobreak = 1;
            break;
        }else{
            c_clrscr();
            if(score>highScore){
                highScore = score;
                printf("You got a new high score of %i! You are amazing!", highScore);
                fyle = fopen("highScore.txt","w");
                fprintf(fyle,"%d", highScore);
                fclose(fyle);
            }else{
                printf("Nice game! You scored %i points", score);
            }
            printf("\nYou were on level %i", level);
            printf("\n\nWould you like to restart? ");

        }
    }
    c_clrscr();
    if(tobreak){
        break;
    }
    }
}
