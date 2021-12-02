class Configure
{
    //the color of the player
    int[] playerColor; //text then background
    playerColor[0] = Codes.greenT; //text color
    playerColor[1] = Codes.reset; //background color
    
    //size of board
    int[] boardSize; //x then y
    boardSize[0] = 30;
    boardSize[1] = 30;
    
    //the starting position that the player is from the top left
    int StartY = boardSize[1]/6*5;
    int StartX = boardSize[0]/2;
    
    
}

