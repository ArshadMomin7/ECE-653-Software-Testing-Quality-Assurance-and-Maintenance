#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <klee/klee.h>

//function prototypes
void checkForWin();

#define MAX_OPTIONS 9

//global variables
char board[MAX_OPTIONS];

char whoWon = ' ';

void checkForWin() {

     int i, 
     contor = 0;
 
     if(board[ 0 ] == 'X' && board[ 1 ] == 'X' && board[ 2 ] == 'X') {

        whoWon = 'X';

     } else if(board[ 3 ] == 'X' && board[ 4 ] == 'X' && board[ 5 ] == 'X') {

        whoWon = 'X';

     } else if(board[ 6 ] == 'X' && board[ 7 ] == 'X' && board[ 8 ] == 'X') {

        whoWon = 'X';

     } else if(board[ 0 ] == 'X' && board[ 3 ] == 'X' && board[ 6 ] == 'X') {

        whoWon = 'X';

     } else if(board[ 1 ] == 'X' && board[ 4 ] == 'X' && board[ 7 ] == 'X') {

        whoWon = 'X';

     } else if(board[ 2 ] == 'X' && board[ 5 ] == 'X' && board[ 8 ] == 'X') {

        whoWon = 'X';

     } else 

     if(board[ 0 ] == 'O' && board[ 1 ] == 'O' && board[ 2 ] == 'O') {

        whoWon = 'O';

     } else if(board[ 3 ] == 'O' && board[ 4 ] == 'O' && board[ 5 ] == 'O') {

        whoWon = 'O';

     } else if(board[ 6 ] == 'O' && board[ 7 ] == 'O' && board[ 8 ] == 'O') {

        whoWon = 'O';

     } else if(board[ 0 ] == 'O' && board[ 3 ] == 'O' && board[ 6 ] == 'O') {

        whoWon = 'O';

     } else if(board[ 1 ] == 'O' && board[ 4 ] == 'O' && board[ 7 ] == 'O') {

        whoWon = 'O';

     } else if(board[ 2 ] == 'O' && board[ 5 ] == 'O' && board[ 8 ] == 'O') {

        whoWon = 'O';

    }     

     //for diagonals
     if(board[ 0 ] == 'X' && board[ 4 ] == 'X' && board[ 8 ] == 'X') {

        whoWon = 'X';

     } else if(board[ 2 ] == 'X' && board[ 4 ] == 'X' && board[ 6 ] == 'X') {

        whoWon = 'X';
     }


     if(board[ 0 ] == 'O' && board[ 4 ] == 'O' && board[ 8 ] == 'O') {

        whoWon = 'O';

     } else if(board[ 2 ] == 'O' && board[ 4 ] == 'O' && board[ 6 ] == 'O') {

        whoWon = 'O';

     }

    int cnt_o = 0;
    int cnt_x = 0;
    for(i = 0; i < 9; i++) {
      if(board[i] == 'X')
        cnt_x++;
    
      if(board[i] == 'O')
        cnt_o++;
    }

    if(!(cnt_x + 1 == cnt_o || cnt_x == cnt_o + 1)) {
      printf("\nInvalid Board!\n");
      return;
    }

     if(whoWon == 'X') {
        printf("\nPlayer1 Won!\n");
        return; 
     }

     if(whoWon == 'O') {
        printf("\nPlayer2 Won!\n");
        return; 
     }

     for(i = 0; i < 9; i++) 
         if(board[i] != ' ') 
               contor++;

     if(contor == 9) {
        whoWon = 'C';
        printf("\nDraw Game!\n");
        return;
     } 
     
}

void displayBoard(char * arr, int size) {

   //   system("cls");
     printf("\t|\t|\n");
     printf("%c\t|%c\t|%c\n", arr[0], arr[1], arr[2]);
     printf("--------|-------|--------\n");
     printf("\t|\t|\n");
     printf("%c\t|%c\t|%c\n", arr[3], arr[4], arr[5]);
     printf("--------|-------|--------\n");
     printf("%c\t|%c\t|%c\n", arr[6], arr[7], arr[8]);
     printf("\t|\t|\n");
};

void writeToFile() {
  FILE *fp;
  fp = fopen("/klee-last/board_stats.txt", "w+");
  if(whoWon == 'C') {
      fprintf(fp, "Draw\n");  
      fputs("Draw\n", fp);
  } else if(whoWon == 'O') {
      fprintf(fp, "Player2\n");
      fputs("Player2\n", fp);
  } else if(whoWon == 'X') {
      fprintf(fp, "Player1\n");
      fputs("Player1\n", fp);
  } else {
      fprintf(fp, "Invalid\n");
      fputs("Invalid\n", fp);
  }
  fclose(fp);
}

int main (int argc, char *argv[])
{
    int i, square;
    int cnt_x = 0;
    int cnt_o = 0;
    for(i = 0; i < 9; i++) {
         board[i] = ' ';
    }  

    // Use Klee's symbolic execution
    klee_make_symbolic(board, MAX_OPTIONS, "board");
    // int size = sizeof board / sizeof board[0];  

    klee_assume(sizeof board / sizeof board[0] >= 5 & sizeof board / sizeof board[0] <= 9);

    for(i = 0; i < MAX_OPTIONS; i++) {
         klee_assume(board[i] == 'X' | board[i] == 'O');
    }  

    for(i = 0; i < 9; i++) {
      if(board[i] == 'X')
        cnt_x++;
      
      if(board[i] == 'O')
        cnt_o++;
    }

   //  klee_assume(cnt_x + 1 == cnt_o | cnt_x == cnt_o + 1); //Uncomment to display only valid combinations

    checkForWin();
    // writeToFile();

   //  displayBoard("OXOXXOOOX", 9);
   
    return 0;
}
