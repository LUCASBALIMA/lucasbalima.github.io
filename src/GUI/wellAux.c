#include<stdio.h>
#include<stdlib.h>
//==============================================================
void exit_tool();
void readWell();
void writeWell();
FILE *arq;
char str[500];
int num_wells;
double xwell[9];
double ywell[9];
double Rate[9];
double rw[9];
double pwf_ini[9];
double pwf_f[9];
double F_pwf[9];
double S[9];
//==============================================================
int main(void){
  readWell();
  writeWell();

  return(0);
}
//==============================================================
void readWell() {
    if((arq=fopen("../../input/well.txt","rt"))==NULL){
        printf("---> File well.txt not found\n\nPress any button to continue\n");
        exit_tool();
    }
  fscanf(arq,"%s %s %d %s %s %s %s %s %s %s %s",
        str,str,&num_wells,str,str,str,str,str,str,str,str);
  for(int i = 0; i < 9; i++){
    fscanf(arq, "%lf %lf %lf %lf %lf %lf %lf %lf",
            &xwell[i], &ywell[i], &Rate[i], &rw[i], &pwf_ini[i], &pwf_f[i], &F_pwf[i], &S[i]);
  }
  fclose(arq);
}
//==============================================================
void writeWell() {
    arq = fopen("wellTemp.txt", "w+");
    if (arq == NULL) {
        printf("---> Failed to open wellTemp.txt for writing.\n");
        exit_tool();
    }
    
    fprintf(arq, "%d\n", num_wells);
    for (int i = 0; i < 9; i++) {
        fprintf(arq, "%.3lf\n", xwell[i]);
    }
    for (int i = 0; i < 9; i++) {
        fprintf(arq, "%.3lf\n", ywell[i]);
    }
    for (int i = 0; i < 9; i++) {
        fprintf(arq, "%.3lf\n", Rate[i]);
    }
    for (int i = 0; i < 9; i++) {
        fprintf(arq, "%.3lf\n", rw[i]);
    }
    for (int i = 0; i < 9; i++) {
        fprintf(arq, "%.3lf\n", pwf_ini[i]);
    }
    for (int i = 0; i < 9; i++) {
        fprintf(arq, "%.3lf\n", pwf_f[i]);
    }
    for (int i = 0; i < 9; i++) {
        fprintf(arq, "%.3lf\n", F_pwf[i]);
    }
    for (int i = 0; i < 9; i++) {
        fprintf(arq, "%.3lf\n", S[i]);
    }
    
    fclose(arq);
}
//==============================================================
void exit_tool(){
  printf("Simulation interrupted.\n");
  exit(1);  
}  