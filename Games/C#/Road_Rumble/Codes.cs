class Codes
{
    public static int reset = 1;
    public static int blackT = 30;
    public static int redT = 31;
  	public static int greenT = 32;
  	public static int yellowT = 33;
  	public static int blueT = 34;
 	public static int magentaT = 35;
 	public static int cyanT = 36;
 	public static int whiteT = 37;
    public static int blackBg = 40;
    public static int redBg = 41;
    public static int greenBg = 42;
    public static int yellowBg = 43;
    public static int blueBg = 44;
    public static int magentaBg = 45;
    public static int cyanBg = 46;
    public static int whiteBg = 47;
    
    public static void setColor(tc, bgc){
        print("\x1b[+"+tc+"m\x1b["+bgc+"m");
    }
}






