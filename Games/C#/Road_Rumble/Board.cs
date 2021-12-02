class Board
{
    public static void makeBoard(out string[,] board, out int[,] tColors, out int[,] bgColors)
    {
        board = new string[Configure.boardSize[1], Configure.boardSize[0]];
        tColors = new int[Configure.boardSize[1], Configure.boardSize[0]];
        bgColors = new int[Configure.boardSize[1], Configure.boardSize[0]];
        for(int y = 0; y <Configure.boardSize[1]; y++)
        {
            for(int x = 0; x <Configure.boardSize[0]; x++)
            {
                board[y, x] = " ";
                tColors[y, x] = Codes.whiteT;
                bgColors[y, x] = Configure.emptyBg;
            }
        }
        
        for(int y = 0; y < Configure.boardSize[1]; y++)
        {
            board[y, 0] = "|";
            board[y, Configure.boardSize[0]-1] = "|";
            bgColors[y, 0] = Configure.wallCols[1];
            tColors[y, 0] = Configure.wallCols[0];
            bgColors[y, Configure.boardSize[0]-1] = Configure.wallCols[1];
            tColors[y, Configure.boardSize[0]-1] = Configure.wallCols[0];
        }
            
        for(int y = 0; y < Configure.boardSize[1]; y++)
        {
            board[y, 0] = "|";
            board[y, Configure.boardSize[0]-1] = "|";
            bgColors[y, 0] = Configure.wallCols[1];
            tColors[y, 0] = Configure.wallCols[0];
            bgColors[y, Configure.boardSize[0]-1] = Configure.wallCols[1];
            tColors[y, Configure.boardSize[0]-1] = Configure.wallCols[0];
        }
        board[Configure.startY, Configure.startX] = "*";
        tColors[Configure.startY, Configure.startX] = Configure.playerCols[0];
        bgColors[Configure.startY, Configure.startX] = Configure.playerCols[1];
        
    }
    
    public static void show(string[,] board, ref string[,] oldBoard, int[,] tColors, int[,] bgColors)
    {
        if(oldBoard != null)
        {
            if(oldBoard != board)
            {
                for(int y = 0; y<Configure.boardSize[1]; y++)
                {
                    for(int x = 0; x<Configure.boardSize[0]; x++){
                        if(board[y, x]!=oldBoard[y, x])
                        {
                            Codes.mvcr(x, y);
                            Codes.setCol(tColors[y, x], bgColors[y, x]);
                            main.print(board[y, x], "");
                            oldBoard[y, x] = board[y, x];
                        }
                    }
                    main.print("");
                }
            }
        }
        else
        {
            oldBoard = board;
            for(int y = 0; y<Configure.boardSize[1]; y++)
            {
                for(int x = 0; x<Configure.boardSize[0]; x++){
                    Codes.mvcr(x, y);
                    Codes.setCol(tColors[y, x], bgColors[y, x]);
                    Codes.setCol(tColors[y, x], tColors[y, x]);
                    main.print(board[y, x], "");
                }
                main.print("");
            }
        }
        
    }
}
