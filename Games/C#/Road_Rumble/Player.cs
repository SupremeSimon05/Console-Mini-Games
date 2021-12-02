class player
{
    public int tc {get; set;}
    public int bgc {get; set;}
    public int pos[] = new int[2] {get; set;}
    public player(){
        this.tc = Configure.playerColor[0];
        this.bgc = Configure.playerColor[1];
        this.pos[0] = Configure.startX;
        this.pos[1] = Configure.startY;
    }
    public void move(int dir)
    {
        switch(dir)
        {
            case 1:
                this.pos[0]--;
            case 2:
                this.pos[0]++;
        }
    }
}

