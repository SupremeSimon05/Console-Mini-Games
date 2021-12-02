#include <stdio.h>
#include <time.h>

enum COLORS
{
  BLACK = 0,
  BLUE = 1,
  GREEN = 2,
  CYAN = 3,
  RED = 4,
  MAGENTA = 5,
  BROWN = 6,
  LIGHTGRAY = 7,
  DARKGRAY = 8,
  LIGHTBLUE = 9,
  LIGHTGREEN = 10,
  LIGHTCYAN = 11,
  LIGHTRED = 12,
  LIGHTMAGENTA = 13,
  YELLOW = 14,
  WHITE = 15,
  BLINK = 128
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
  case BLACK:
    s = "\x1b[30m";
    break;

  case BLUE:
    s = "\x1b[34m";
    break;

  case GREEN:
    s = "\x1b[32m";
    break;

  case CYAN:
    s = "\x1b[36m";
    break;

  case RED:
    s = "\x1b[31;1m";
    break;

  case MAGENTA:
    s = "\x1b[35m";
    break;

  case BROWN:
    s = "\x1b[31m";
    break;

  case LIGHTGRAY:
    s = "\x1b[30;1m";
    break;

  case DARKGRAY:
    s = "\x1b[30m";
    break;

  case LIGHTBLUE:
    s = "\x1b[34;1m";
    break;

  case LIGHTGREEN:
    s = "\x1b[32,1m";;
    break;

  case LIGHTCYAN:
    s = "\x1b[36;1m";
    break;

  case LIGHTRED:
    s = "\x1b[31;1m";
    break;

  case LIGHTMAGENTA:
    s = "\x1b[35;1m";
    break;

  case YELLOW:
    s = "\x1b[33;1m";
    break;

  case WHITE:
    s = "\x1b[37;1m";
    break;

  case BLINK:
    s = "\x1b[30m";
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
            if(board[a][b] == "A" || board[a][b] == "*"){
                c_textcolor(BLUE);
            }else if(board[a][b] == "=" || board[a][b] == "T"){
                c_textcolor(GREEN);
            }else if(board[a][b] == "(" || board[a][b] == ")"){
                c_textcolor(YELLOW);
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
                if(board[a][b] == "A" || board[a][b] == "*"){
                    c_textcolor(BLUE);
                }else if(board[a][b] == "=" || board[a][b] == "T"){
                    c_textcolor(GREEN);
                }else if(board[a][b] == "(" || board[a][b] == ")"){
                    c_textcolor(YELLOW);
                }else if(board[a][b] == "#"){
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
    int SIZEY = 15;
    int SIZEX = 50;
    int position[2];
    position[0] = 5;
    position[1] = SIZEY-(SIZEY/4)-3;
    int a;
    int wood = 0;
    int money = 0;
    int numHouses = 0;
    int level = 1;
    char * homeBase[SIZEY][SIZEX];
    char * board[SIZEY][SIZEX];
    char * oldBoard[SIZEY][SIZEX];
    int perlinum = 3;
    int toDig = 0;
    int dist = 0;
    
    //Start of directions in ascii
    int up = 119;
    int right = 100;
    int down = 115;
    int left = 97;
    int SPACE = 32;
    int B = 98;
    int S = 115; 
    int E = 101;
    int Q = 113;
    int upcasD  = 68;
    int upcasA = 65;
    int upcasS = 83;
    //End of directions in ascii
    
    
    c_clrscr();
    c_gotoxy(0,0);
    int seed;
    printf("What would you like to have as the seed? ");
    scanf("%d", &seed);
    if(seed == EOF){
        seed = rand()-1;
    }
    c_clrscr();
    c_gotoxy(0,0);
    
    //Start of board making
    for(a = 0; a<SIZEY; a++){
        int b;
        for(b = 0; b<SIZEX; b++){
            board[a][b] = " ";
        }
    }
    printf("%s\n", board[0][2]);
    for(a = 0; a<perlinum; a++){
        int b;
        for(b=0; b<SIZEX; b++){
            board[SIZEY-a-1][b] = "=";
        }
    }
    srand(seed);
    for(a=0; a<SIZEY/5; a++){
        int b;
        for(b=0; b<SIZEX; b++){
            if(rand()%4 == 0){
                board[a][b] = "C";
            }
        }
    }
    //End of board making
    board[SIZEY-4][0] = "A";
    
    for(a = 0; a<SIZEY-1; a++){
        int b;
        for(b = 0; b<SIZEX-1; b++){
            oldBoard[a][b] = board[a][b];
        }
    }
    for(a = 0; a<SIZEY-1; a++){
        int b;
        for(b = 0; b<SIZEX-1; b++){
            homeBase[a][b] = board[a][b];
        }
    }
    
    //Save stuffs
    c_clrscr();
    c_gotoxy(0,0);
    FILE *fyle;
    printf("What name do you want to save/load to/from? ");
    char whatFile[50];
    scanf("%s", whatFile);
    if((fyle = fopen(whatFile, "r")) == NULL){
        fyle = fopen(whatFile, "w");
        fprintf(fyle, "%d,%d,%d,%d", 0, 0, 1, 0);
        fprintf(fyle, "\n");
        for(a = 0; a<SIZEY; a++){
            for(int b = 0; b<SIZEX; b++){
                fprintf(fyle, "'%i'", homeBase[a][b]);
            }
        }
        fclose(fyle);
    }else{
        fscanf(fyle, "%d,%d,%d,%d", &wood, &money, &level, &dist);
        fscanf(fyle, "\n");
        for(a = 0; a<SIZEY; a++){
            for(int b = 0; b<SIZEX; b++){
                fscanf(fyle, "'%i'", &homeBase[a][b]);
            }
        }
        fclose(fyle);
        for(a=0; a<dist; a++){
            rand();
        }
    }
    printf("\x1b[?25l");
    c_clrscr();
    c_gotoxy(0,2);
    
    showBoard(SIZEX, SIZEY, board);
    int key = 0;
    
    //chooses how fast the board updates 
    int SPEED = 50;
    int jumping = 0;
    
    int atHomeBase = 1;
    int tillHomeBase = 0;
    char *underPlayer = " ";
    char *dir = "r";
    int throwing = 0;
    
    //direction, self
    int dashing[2];
    dashing[0] = 1;
    dashing[1] = 0;
    
    //positions, direction, bouce, rendering.
    int rang[5];
    rang[0] = position[0];
    rang[1] = position[1];
    rang[2] = 1;
    rang[3] = 0;
    rang[4] = 0;
    
    //positions, direction, rendering
    int simp[4];
    simp[0] = position[0];
    simp[1] = position[1];
    simp[2] = 1;
    simp[3] = 0;
    
    //positions, direction, rendering, if over tree
    int nosimp[5];
    nosimp[0] = position[0];
    nosimp[1] = position[1];
    nosimp[2] = 1;
    nosimp[3] = 0;
    nosimp[4] = 0;
    
    int oldSpeed = SPEED;
    int autoBuild = 0;
    int BuyTimes = 0;
    
    //game
    while(1){
        msleep(SPEED);
        c_textcolor(BROWN);
        c_gotoxy(0,0);
        printf("                               ");
        c_gotoxy(0,0);
        printf("                               ");
        c_gotoxy(0,0);
        printf("                               ");
        c_gotoxy(0,0);
        printf("Wood: %i, ", wood);
        c_textcolor(YELLOW);
        printf("Money: %i, ", money);
        c_textcolor(GREEN);
        printf("Level: %i ", level);
        //Start of updating board
        if(atHomeBase){
            for(a=0; a<SIZEY-1; a++){
                int b;
                for(b=0; b<SIZEX-1; b++){
                    board[a][b] = homeBase[a][b];
                }
            }
        }
        board[position[1]][position[0]] = "*";
        
        if(rang[4]){
            if((rang[2] && !rang[3]) || (!rang[2] && rang[3])){
                board[rang[1]][rang[0]] = "(";
            }else{
                board[rang[1]][rang[0]] = ")";
            }
        }
        if(simp[3]){
            board[simp[1]][simp[0]] = "#";
        }
        
        if(nosimp[3]){
            board[nosimp[1]][nosimp[0]] = "#";
        }
        
        //End of updating board
        
        reprintBoard(SIZEX, SIZEY, board, oldBoard);
        for(a = 0; a<SIZEY-1; a++){
            int b;
            for(b = 0; b<SIZEX-1; b++){
                oldBoard[a][b] = board[a][b];
            }
        }
        //Start of movements
        if(wood<1200){
            autoBuild = 0;
            SPEED = oldSpeed;
        }
        
        if(position[0] == SIZEX-2 && position[1] == SIZEX-3){
            autoBuild = 0;
            SPEED = oldSpeed;
        }
        
        if(c_kbhit() || dashing[1] || autoBuild){
            if(dashing[1]){
                if(dashing[0]){
                    key = right;
                }else{
                    key = left;
                }
            }else if(autoBuild){
                SPEED = 0;
                if(wood<10000){
                    if(position[0]<SIZEX-2){
                        if(rand()%10 == 0){
                            key = right;
                        }else{
                            if(rand()%10 == 0){
                                key = left;
                            }else{
                                key = SPACE;
                            }
                        }
                    }
                    if(rand()%15 == 0){
                        key = down;
                    }else if(rand()%20 == 0){
                        key = up;
                    }
                }else if(wood>=10000){
                    for(a=0; a<SIZEY-3; a++){
                        for(int b=0; b<SIZEX-2; b++){
                            for(int c=0; c<9; c++){
                                position[1] = a;
                                position[0] = b;
                                if(homeBase[position[1]][position[0]] != "A"){
                                    if((homeBase[position[1]][position[0]] == " " || homeBase[position[1]][position[0]] == "C") && wood >= 100){
                                        homeBase[position[1]][position[0]] = "1";
                                        underPlayer = "1";
                                        wood-=100;
                                    }else if(homeBase[position[1]][position[0]] == "1" && wood >= 150){
                                        homeBase[position[1]][position[0]] = "2";
                                        underPlayer = "2";
                                        wood-=150;
                                    }else if(homeBase[position[1]][position[0]] == "2" && wood >= 225){
                                        homeBase[position[1]][position[0]] = "3";
                                        underPlayer = "3";
                                        wood-=225;
                                    }else if(homeBase[position[1]][position[0]] == "3" && wood >= 325){
                                        homeBase[position[1]][position[0]] = "4";
                                        underPlayer = "4";
                                        wood-=325;
                                    }else if(homeBase[position[1]][position[0]] == "4" && wood >= 450){
                                        homeBase[position[1]][position[0]] = "5";
                                        underPlayer = "5";
                                        wood-=450;
                                    }else if(homeBase[position[1]][position[0]] == "5" && wood >= 600){
                                        homeBase[position[1]][position[0]] = "6";
                                        underPlayer = "6";
                                        wood-=600;
                                    }else if(homeBase[position[1]][position[0]] == "6" && wood >= 775){
                                        homeBase[position[1]][position[0]] = "7";
                                        underPlayer = "7";
                                        wood-=775;
                                    }else if(homeBase[position[1]][position[0]] == "7" && wood >= 975){
                                        homeBase[position[1]][position[0]] = "8";
                                        underPlayer = "8";
                                        wood-=975;
                                    }else if(homeBase[position[1]][position[0]] == "8" && wood >= 1200){
                                        homeBase[position[1]][position[0]] = "9";
                                        underPlayer = "9";
                                        wood-=1200;
                                    }else if(homeBase[position[1]][position[0]] == "9"){
                                        money++;
                                    }
                                }
                            }
                        }
                    }
                    autoBuild = 0;
                    SPEED = oldSpeed;
                    key = SPACE;
                }
            }else{
                key = getchar();
            }
            
            if(key == 27){
                fyle = fopen(whatFile, "w");
                fprintf(fyle, "%d,%d,%d,%d", wood, money, level, dist);
                fprintf(fyle, "\n");
                for(a = 0; a<SIZEY; a++){
                    for(int b = 0; b<SIZEX; b++){
                        fprintf(fyle, "'%i'", homeBase[a][b]);
                    }
                }
                fclose(fyle);
                break;
            }else if(key == up){
                if(board[position[1]+1][position[0]] != " " && board[position[1]+1][position[0]] != " "){
                    jumping = 3;
                }
            }
            if(key == right){
                dir = "r";
                if(board[position[1]][position[0]+1] != "="){
                    board[position[1]][position[0]] = underPlayer;
                    position[0]++;
                    if((jumping>0 || board[position[1]+1][position[0]] == " ") && !atHomeBase && board[position[1]][position[0]+1] == " "){
                        position[0]++;
                    }
                    underPlayer = board[position[1]][position[0]];
                }else if((board[position[1]-1][position[0]+1] == " " || board[position[1]-1][position[0]+1] == "T" || board[position[1]-1][position[0]+1] == "C") && !dashing[1]){
                    board[position[1]][position[0]] = " ";
                    position[0]++;
                    position[1]--;
                    underPlayer = board[position[1]][position[0]];
                }else if(toDig && board[position[1]][position[0]+1] == "="){
                    if(board[position[1]-1][position[0]+1] == "T"){
                        underPlayer = " ";
                    }
                    board[position[1]][position[0]] = underPlayer;
                    position[0]++;
                    underPlayer = " ";
                    toDig = 0;
                }else{
                    dashing[0] = 1;
                    dashing[1] = 0;
                }
            }
            if(key == left){
                dir = "l";
                if(position[0]>0 || !atHomeBase){
                    if(board[position[1]][position[0]-1] != "="){
                        board[position[1]][position[0]] = underPlayer;
                        position[0]--;
                        if((jumping>0 || board[position[1]+1][position[0]] == " ") && position[0]>0 && board[position[1]][position[0]-1] == " "){
                            position[0]--;
                        }
                        underPlayer = board[position[1]][position[0]];
                    }else if((board[position[1]-1][position[0]-1] == " " || board[position[1]-1][position[0]-1] == "T" || board[position[1]-1][position[0]-1] == "C") && !dashing[1]){
                        board[position[1]][position[0]] = underPlayer;
                        position[0]--;
                        position[1]--;
                        underPlayer = board[position[1]][position[0]];
                    }else if(toDig && board[position[1]][position[0]-1] == "="){
                        if(board[position[1]-1][position[0]-1] == "T"){
                            underPlayer = " ";
                        }
                        board[position[1]][position[0]] = underPlayer;
                        position[0]--;
                        underPlayer = " ";
                        toDig = 0;
                    }else{
                        dashing[0] = 1;
                        dashing[1] = 0;
                    }
                }else{
                    dashing[1] = 0;
                    dashing[0] = 1;
                }
            }
            if(key == down){
                if(board[position[1]+1][position[0]] != " " && board[position[1]+1][position[0]] != "="){
                    board[position[1]][position[0]] = underPlayer;
                    position[1]++;
                    underPlayer = board[position[1]][position[0]];
                }else if(toDig && board[position[1]+1][position[0]] == "="){
                    if(underPlayer == "T"){
                        underPlayer = " ";
                    }
                    board[position[1]][position[0]] = underPlayer;
                    position[1]++;
                    underPlayer = " ";
                    toDig = 0;
                }
            }
            if(key == SPACE && atHomeBase && homeBase[position[1]][position[0]] != "A"){
                if((homeBase[position[1]][position[0]] == " " || homeBase[position[1]][position[0]] == "C") && wood >= 100){
                    homeBase[position[1]][position[0]] = "1";
                    underPlayer = "1";
                    wood-=100;
                }else if(homeBase[position[1]][position[0]] == "1" && wood >= 150){
                    homeBase[position[1]][position[0]] = "2";
                    underPlayer = "2";
                    wood-=150;
                }else if(homeBase[position[1]][position[0]] == "2" && wood >= 225){
                    homeBase[position[1]][position[0]] = "3";
                    underPlayer = "3";
                    wood-=225;
                }else if(homeBase[position[1]][position[0]] == "3" && wood >= 325){
                    homeBase[position[1]][position[0]] = "4";
                    underPlayer = "4";
                    wood-=325;
                }else if(homeBase[position[1]][position[0]] == "4" && wood >= 450){
                    homeBase[position[1]][position[0]] = "5";
                    underPlayer = "5";
                    wood-=450;
                }else if(homeBase[position[1]][position[0]] == "5" && wood >= 600){
                    homeBase[position[1]][position[0]] = "6";
                    underPlayer = "6";
                    wood-=600;
                }else if(homeBase[position[1]][position[0]] == "6" && wood >= 775){
                    homeBase[position[1]][position[0]] = "7";
                    underPlayer = "7";
                    wood-=775;
                }else if(homeBase[position[1]][position[0]] == "7" && wood >= 975){
                    homeBase[position[1]][position[0]] = "8";
                    underPlayer = "8";
                    wood-=975;
                }else if(homeBase[position[1]][position[0]] == "8" && wood >= 1200){
                    homeBase[position[1]][position[0]] = "9";
                    underPlayer = "9";
                    wood-=1200;
                }else if(homeBase[position[1]][position[0]] == "9"){
                    money++;
                }
            }
            if(key == SPACE && underPlayer == "T"){
                underPlayer = " ";
                wood += 10*level;
            }
            if(key == B && money>=10*(BuyTimes+1)){
                money-=10*(BuyTimes+1);
                wood+=BuyTimes+1;
                BuyTimes++;
            }else{
                BuyTimes = 0;
            }
            if(key == S){
                fyle = fopen(whatFile, "w");
                fprintf(fyle, "%d,%d,%d,%d", wood, money, level, dist);
                fprintf(fyle, "\n");
                for(a = 0; a<SIZEY; a++){
                    for(int b = 0; b<SIZEX; b++){
                        fprintf(fyle, "'%i'", homeBase[a][b]);
                    }
                }
                fclose(fyle);
            }
            if(key == E && !rang[4]){
                if(dir == "r" && board[position[1]][position[0]+1] != "="){
                    throwing = 5;
                    rang[0] = position[0];
                    rang[1] = position[1];
                    rang[2] = 1;
                    rang[3] = 0;
                    rang[4] = 1;
                }
                if(dir == "l" && board[position[1]][position[0]-1] != "="){
                    throwing = 5;
                    rang[0] = position[0];
                    rang[1] = position[1];
                    rang[2] = 0;
                    rang[3] = 0;
                    rang[4] = 1;
                }
            }
            if(key == Q && !atHomeBase && !toDig){
                toDig = 1;
            }else if(key == Q && !atHomeBase && toDig){
                toDig = 0;
            }
            if(key == upcasA){
                dashing[0] = 0;
                dashing[1] = 1;
            }
            if(key == upcasD){
                dashing[0] = 1;
                dashing[1] = 1;
            }
            if(key == upcasS && atHomeBase){
                autoBuild = 1;
            }
        }
        
        if(throwing>0 && rang[4]){
            throwing--;
            if(rang[2]){
                if(board[rang[1]][rang[0]+1] != "="){
                    if(board[rang[1]][rang[0]+1] == "T"){
                        wood+=10*level;
                    }
                    board[rang[1]][rang[0]] = " ";
                    rang[0]++;
                }else{
                    throwing = 0;
                    rang[3] = 1;
                }
            }else{
                if(board[rang[1]][rang[0]-1] != "="){
                    if(board[rang[1]][rang[0]-1] == "T"){
                        wood+=10*level;
                    }
                    board[rang[1]][rang[0]] = " ";
                    rang[0]--;
                }else{
                    throwing = 0;
                    rang[3] = 1;
                }
            }
        }else{
            rang[3] = 1;
        }
        
        if(rang[3] && rang[4]){
            if(rang[2]){
                if(board[rang[1]][rang[0]-1] != "="){
                    board[rang[1]][rang[0]] = " ";
                    rang[0]--;
                }else{
                    board[rang[1]][rang[0]] = " ";
                    rang[4] = 0;
                    rang[3] = 0;
                }
            }else{
                if(board[rang[1]][rang[0]+1] != "="){
                    board[rang[1]][rang[0]] = " ";
                    rang[0]++;
                }else{
                    board[rang[1]][rang[0]] = " ";
                    rang[4] = 0;
                    rang[3] = 0;
                }
            }
        }
        
        if(rang[0]<1 || rang[0]>SIZEX-2){
            rang[4] = 0;
            rang[3] = 0;
            throwing = 0;
        }
        
        if(rang[0] == position[0] && rang[1] == position[1]){
            rang[4] = 0;
            rang[3] = 0;
        }
        
        if(jumping>0){
            if(position[1]>0){
                if(board[position[1]-1][position[0]] != "="){
                    board[position[1]][position[0]] = underPlayer;
                    position[1]--;
                    underPlayer = board[position[1]][position[0]];
                }else if(toDig){
                    board[position[1]][position[0]] = underPlayer;
                    position[1]--;
                    underPlayer = " ";
                }
                if(jumping == 1){
                    toDig = 0;
                }
            }
            jumping--;
        }else if((board[position[1]+1][position[0]] == " " || board[position[1]+1][position[0]] == "C" || board[position[1]+1][position[0]] == "T") && !dashing[1]){
            board[position[1]][position[0]] = underPlayer;
            position[1]++;
            underPlayer = board[position[1]][position[0]];
        }
        //End of movements
        
        //Finds the amount of houses built
        numHouses = 0;
        for(a = 0; a<SIZEY; a++){
            int b;
            for(b=0; b<SIZEX; b++){
                if(homeBase[a][b] == "1"){
                    numHouses+=1;
                }else if(homeBase[a][b] == "2"){
                    numHouses+=2;
                }else if(homeBase[a][b] == "3"){
                    numHouses+=3;
                }else if(homeBase[a][b] == "4"){
                    numHouses+=4;
                }else if(homeBase[a][b] == "5"){
                    numHouses+=5;
                }else if(homeBase[a][b] == "6"){
                    numHouses+=6;
                }else if(homeBase[a][b] == "7"){
                    numHouses+=7;
                }else if(homeBase[a][b] == "8"){
                    numHouses+=8;
                }else if(homeBase[a][b] == "9"){
                    numHouses+=9;
                }
            }
        }
        
        //checks for player dying
        if(simp[0] == position[0] && simp[1] == position[1] && simp[3]){
            for(a=0; a<SIZEY-4; a++){
                board[a][SIZEX-1] = " ";
            }
            position[1] = SIZEY-4;
            position[0] = 0;
            perlinum = 3;
            atHomeBase = 1;
            simp[3] = 0;
            if(nosimp[3]){
                nosimp[3] = 0;
                board[nosimp[1]][nosimp[0]] = " ";
                nosimp[0] = SIZEX-1;
                nosimp[1] = SIZEY-1;
            }
            board[simp[1]][simp[0]] = " ";
            simp[0] = SIZEX-1;
            simp[1] = SIZEY-1;
        }
        if(nosimp[0] == position[0] && nosimp[1] == position[1] && nosimp[3]){
            for(a=0; a<SIZEY-4; a++){
                board[a][SIZEX-1] = " ";
            }
            position[1] = 5;
            perlinum = 3;
            atHomeBase = 1;
            nosimp[3] = 0;
            if(simp[3]){
                simp[3] = 0;
                board[nosimp[1]][nosimp[0]] = " ";
                nosimp[0] = SIZEX-1;
                nosimp[1] = SIZEY-1;
            }
            board[simp[1]][simp[0]] = " ";
            simp[0] = SIZEX-1;
            simp[1] = SIZEY-1;
        }
        
        //simp movements
        if((position[0] == simp[0] && simp[3] && position[1]+1 == simp[1]) || (simp[0] == rang[0] && simp[1] == rang[1] && rang[4] && simp[3])){
            simp[3] = 0;
            board[simp[1]][simp[0]] = " ";
            simp[0] = SIZEX-1;
            simp[1] = SIZEY-1;
            money+=level*2;
        }
        if(simp[3] && board[simp[1]+1][simp[0]] == " "){
            board[simp[1]][simp[0]] = " ";
            simp[1]++;
        }
        if(simp[0]<1 && simp[3]){
            simp[3] = 0;
            board[simp[1]][simp[0]] = " ";
            simp[0] = SIZEX-1;
            simp[1] = SIZEY-1;
        }else if(simp[0]>SIZEX-2 && simp[3]){
            simp[2] = 0;
            simp[0] = SIZEX-2;
        }else if(simp[1]>SIZEY-1 && simp[3]){
            simp[3] = 0;
            board[simp[1]][simp[0]] = " ";
            simp[0] = SIZEX-1;
            simp[1] = SIZEY-1;
        }else if(simp[1]<0 && simp[3]){
            simp[3] = 0;
            board[simp[1]][simp[0]] = " ";
            simp[0] = SIZEX-1;
            simp[1] = SIZEY-1;
        }
        
        if(simp[3]){
            if(simp[2]){
                if(board[simp[1]][simp[0]+1] == " " || board[simp[1]][simp[0]+1] == "*"){
                    board[simp[1]][simp[0]] = " ";
                    simp[0]++;
                }else{
                    simp[2] = 0;
                }
            }else{
                if(board[simp[1]][simp[0]-1] == " " || board[simp[1]][simp[0]-1] == "*"){
                    board[simp[1]][simp[0]] = " ";
                    simp[0]--;
                }else{
                    simp[2] = 1;
                }
            }
        }
        //end of simp movements
        
        //nosimp movements
        if((position[0] == nosimp[0] && nosimp[3] && position[1]+1 == nosimp[1]) || (nosimp[0] == rang[0] && nosimp[1] == rang[1] && rang[4] && nosimp[3])){
            nosimp[3] = 0;
            board[nosimp[1]][nosimp[0]] = " ";
            nosimp[0] = SIZEX-1;
            nosimp[1] = SIZEY-1;
            money+=level*2;
        }
        if(nosimp[3] && board[nosimp[1]+1][nosimp[0]] == " "){
            board[nosimp[1]][nosimp[0]] = " ";
            nosimp[1]++;
        }
        if(nosimp[0]<1 && simp[3]){
            nosimp[3] = 0;
            board[nosimp[1]][nosimp[0]] = " ";
            nosimp[0] = SIZEX-1;
            nosimp[1] = SIZEY-1;
        }else if(nosimp[0]>SIZEX-2 && nosimp[3]){
            nosimp[3] = 0;
            board[nosimp[1]][nosimp[0]] = " ";
            nosimp[0] = SIZEX-1;
            nosimp[1] = SIZEY-1;
        }else if(nosimp[1]>SIZEY-1 && nosimp[3]){
            nosimp[3] = 0;
            board[nosimp[1]][nosimp[0]] = " ";
            nosimp[0] = SIZEX-1;
            nosimp[1] = SIZEY-1;
        }else if(nosimp[1]<0 && nosimp[3]){
            nosimp[3] = 0;
            board[nosimp[1]][nosimp[0]] = " ";
            nosimp[0] = SIZEX-1;
            nosimp[1] = SIZEY-1;
        }
        if(nosimp[3]){
            if(nosimp[2]){
                if(board[nosimp[1]][nosimp[0]+1] != "="){
                    if(nosimp[4]){
                        board[nosimp[1]][nosimp[0]] = "T";
                    }else{
                        board[nosimp[1]][nosimp[0]] = " ";
                    }
                    if(board[nosimp[1]][nosimp[0]+1] == "T"){
                        nosimp[4] = 1;
                    }else{
                        nosimp[4] = 0;
                    }
                    nosimp[0]++;
                }else if(board[nosimp[1]-1][nosimp[0]+1] != "="){
                    if(nosimp[4]){
                        board[nosimp[1]][nosimp[0]] = "T";
                    }else{
                        board[nosimp[1]][nosimp[0]] = " ";
                    }
                    if(board[nosimp[1]-1][nosimp[0]+1] == "T"){
                        nosimp[4] = 1;
                    }else{
                        nosimp[4] = 0;
                    }
                    nosimp[0]++;
                    nosimp[1]--;
                }else{
                    nosimp[2] = 0;
                }
            }else{
                if(board[nosimp[1]][nosimp[0]-1] != "="){
                    if(nosimp[4]){
                        board[nosimp[1]][nosimp[0]] = "T";
                    }else{
                        board[nosimp[1]][nosimp[0]] = " ";
                    }
                    if(board[nosimp[1]][nosimp[0]-1] == "T"){
                        nosimp[4] = 1;
                    }else{
                        nosimp[4] = 0;
                    }
                    nosimp[0]--;
                }else if(board[nosimp[1]-1][nosimp[0]-1] != "="){
                    if(nosimp[4]){
                        board[nosimp[1]][nosimp[0]] = "T";
                    }else{
                        board[nosimp[1]][nosimp[0]] = " ";
                    }
                    if(board[nosimp[1]-1][nosimp[0]-1] == "T"){
                        nosimp[4] = 1;
                    }else{
                        nosimp[4] = 0;
                    }
                    nosimp[0]--;
                    nosimp[1]--;
                }else{
                    nosimp[2] = 1;
                }
            }
        }
        //end of nosimp movements
        
        //Scrolling stuff
        
        //X axis
        if(position[0]>SIZEX-2 && !atHomeBase){
            position[0]=SIZEX-3;
        }
        if(atHomeBase){
            if(position[0]>SIZEX-2){
                position[0]=SIZEX-3;
                char * newBoard[SIZEY][SIZEX];
                for(a=0; a<SIZEX; a++){
                    int b;
                    for(b = 0; b<SIZEY; b++){
                        newBoard[b][a] = board[b][a+1];
                    }
                }
                for(a=0; a<SIZEY/5; a++){
                    if(rand()%6 == 0){
                        newBoard[a][SIZEX-2] = "C";
                    }
                }
                for(a=0; a<SIZEY; a++){
                    int b;
                    for(b = 0; b<SIZEX-1; b++){
                        board[a][b] = newBoard[a][b];
                    }
                }
                atHomeBase = 0;
            }
            nosimp[0]--;
            simp[0]--;
            tillHomeBase++;
            dist++;
        }else if(position[0]>SIZEX/4){
            dist++;
            nosimp[0]--;
            simp[0]--;
            position[0]--;
            char * newBoard[SIZEY][SIZEX];
            for(a=0; a<SIZEX-1; a++){
                int b;
                for(b = 0; b<SIZEY; b++){
                    newBoard[b][a] = board[b][a+1];
                }
            }
            for(a = 0; a<SIZEY; a++){
                board[SIZEY-a-1][SIZEX-1] = " ";
            }
            for(a=0; a<3; a++){
                if(perlinum>0 && rand()%3 == 0){
                    perlinum--;
                }
                if(rand()%3 == 0){
                    perlinum++;
                }
            }
            for(a=0; a<SIZEY/5; a++){
                if(perlinum<SIZEY-3 && rand()%6 == 0){
                    newBoard[a][SIZEX-2] = "C";
                }
            }
            for(a = 0; a<SIZEY; a++){
                board[a][SIZEX-1] = " ";
            }
            for(a = 0; a<perlinum; a++){
                board[SIZEY-a-1][SIZEX-1] = "=";
            }
            if(rand()%3 == 0){
                if(newBoard[SIZEY-perlinum][SIZEX-2] == "="){
                    newBoard[SIZEY-perlinum-1][SIZEX-2] = "T";
                }
            }
            
            if(rand()%4 == 0 && !simp[3] && position[0]<SIZEX/2){
                newBoard[SIZEY-perlinum-1][SIZEX-3] = "#";
                simp[3] = 1;
                simp[1] = SIZEY-perlinum-1;
                simp[0] = SIZEX-3;
                simp[2] = 0;
            }
            
            if(rand()%7 == 0 && !nosimp[3] && position[0]<SIZEX/2){
                newBoard[SIZEY-perlinum-1][SIZEX-2] = "#";
                nosimp[3] = 1;
                nosimp[1] = SIZEY-perlinum-1;
                nosimp[0] = SIZEX-2;
                nosimp[2] = 0;
            }
            
            
            
            for(a=0; a<SIZEY; a++){
                int b;
                for(b = 0; b<SIZEX-1; b++){
                    board[a][b] = newBoard[a][b];
                }
            }
            tillHomeBase++;
        }
        if(tillHomeBase<=1){
            perlinum = 3;
            atHomeBase = 1;
            for(a=0; a<SIZEY-1; a++){
                board[a][SIZEX-1] = " ";
            }
            for(a=0; a<3; a++){
                board[SIZEY-a-1][SIZEX-1] = "=";
            }
        }
        if(!atHomeBase && position[0]<=1){
            nosimp[0]++;
            simp[0]++;
            perlinum = SIZEY-position[1];
            position[0]++;
            char * newBoard[SIZEY][SIZEX];
            for(a=0; a<SIZEX-1; a++){
                int b;
                for(b = 0; b<SIZEY; b++){
                    newBoard[b][a+1] = board[b][a];
                }
            }
            if(tillHomeBase>SIZEX-1){
                tillHomeBase = SIZEX-1;
                for(a=0; a<SIZEY-1; a++){
                    newBoard[a][0] = " ";
                }
                for(a=0; a<3; a++){
                    newBoard[SIZEY-a-1][0] = "=";
                }
            }else{
                for(a=0; a<SIZEY; a++){
                    newBoard[a][0] = homeBase[a][tillHomeBase-1];
                }
            }
            for(a=0; a<SIZEY; a++){
                int b;
                for(b = 0; b<SIZEX; b++){
                    board[a][b] = newBoard[a][b];
                }
            }
            tillHomeBase--;
        }
        
        //Y axis
        
        if(position[1]<SIZEY/4 && !atHomeBase){
            nosimp[1]++;
            simp[1]++;
            position[1]++;
            perlinum--;
            char * newBoard[SIZEY][SIZEX];
            for(a=0; a<SIZEX; a++){
                int b;
                for(b = 0; b<SIZEY; b++){
                    newBoard[b][a] = board[b-1][a];
                }
            }
            
            for(a=0; a<SIZEX; a++){
                newBoard[0][a] = " ";
            }
            
            for(a=0; a<SIZEX; a++){
                if(perlinum<SIZEY-3 && rand()%6 == 0){
                    newBoard[0][a] = "C";
                }
            }
            
            for(a=0; a<SIZEY; a++){
                int b;
                for(b = 0; b<SIZEX; b++){
                    board[a][b] = newBoard[a][b];
                }
            }
        }else if(position[1]>SIZEY-2){
            nosimp[1]--;
            simp[1]--;
            perlinum++;
            char * newBoard[SIZEY][SIZEX];
            for(a=0; a<SIZEX-1; a++){
                int b;
                for(b = 0; b<SIZEY-1; b++){
                    newBoard[b][a] = board[b+1][a];
                }
            }
            if(tillHomeBase>SIZEY-1){
                tillHomeBase = SIZEY-1;
                for(a=0; a<SIZEX; a++){
                    newBoard[SIZEY-1][a] = " ";
                }
            }else{
                for(a=0; a<SIZEX-1; a++){
                    newBoard[SIZEY-1][a] = homeBase[SIZEY-tillHomeBase-1][a];
                }
            }
            
            for(a=0; a<SIZEY; a++){
                int b;
                for(b = 0; b<SIZEX-1; b++){
                    board[a][b] = newBoard[a][b];
                }
            }
            tillHomeBase--;
            if(position[1]>SIZEY-1){
                position[1] = SIZEY-2;
            }
            if(board[position[1]+1][position[0]] == "="){
                position[1]-=3;
            }
        }
        
        
        //End of scrolling
        
        //Gives you money at random times for you owning houses
        if(clock()%200 == 0){
            money+=numHouses;
        }
        
        if(numHouses>(SIZEX-3)*(SIZEY-5)*8){
            level++;
            for(a = 0; a<SIZEY; a++){
                int b;
                for(b = 0; b<SIZEX; b++){
                    homeBase[a][b] = " ";
                }
            }
            printf("%s\n", homeBase[0][2]);
            for(a = 0; a<3; a++){
                int b;
                for(b=0; b<SIZEX; b++){
                    homeBase[SIZEY-a-1][b] = "=";
                }
            }
            srand(seed+level);
            for(a=0; a<SIZEY/5; a++){
                int b;
                for(b=0; b<SIZEX; b++){
                    if(rand()%4 == 0){
                        homeBase[a][b] = "C";
                    }
                }
            }
        }
        
        //Fixes the board if you're at hb
        if(atHomeBase){
            if(simp[3]){
                simp[3] = 0;
                simp[0] = SIZEX-1;
                simp[1] = SIZEY-1;
            }
            if(nosimp[3]){
                nosimp[3] = 0;
                nosimp[0] = SIZEX-1;
                nosimp[1] = SIZEY-1;
            }
            if(position[1]>SIZEY-4){
                position[1] = SIZEY-4;
            }
            for(a=0; a<SIZEY; a++){
                for(int b=0; b<SIZEX; b++){
                    if(board[a][b] == "T"){
                        board[a][b] = " ";
                        homeBase[a][b] = " ";
                    }
                }
            }
            for(a=0; a<3; a++){
                for(int b=0; b<SIZEX; b++){
                    board[SIZEY-a-1][b] = "=";
                    homeBase[SIZEY-a-1][b] = "=";
                    oldBoard[SIZEY-a-1][b] = "+";
                }
            }
            for(a=0; a<SIZEX; a++){
                board[SIZEY-1][a] = "=";
                homeBase[SIZEY-1][a] = "=";
                oldBoard[SIZEY-1][a] = "+";
            }
            for(a=0; a<SIZEY; a++){
                oldBoard[a][SIZEX-1] = "+";
            }
            board[SIZEY-4][0] = "A";
            homeBase[SIZEY-4][0] = "A";
        }
        
        //forces reprint at random times so unchanging parts can update
        if(clock()%50){
            for(a=0; a<SIZEY; a++){
                oldBoard[a][SIZEX-1] = "+";
            }
            for(a=0; a<SIZEX; a++){
                oldBoard[SIZEY-1][a] = "+";
            }
            for(a=0; a<SIZEY; a++){
                oldBoard[a][0] = "+";
            }
            for(a=0; a<SIZEX; a++){
                oldBoard[0][a] = "+";
            }
        }
    }
}
