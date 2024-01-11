#include<stdio.h>
#include<stdlib.h>

void exit_tool();
void readHeat();
void writeHeat();
FILE *arq;
char str[500];
int num_heats;
double xheat[8];
double yheat[8];
double Heat[8];

int main(void){
  readHeat();
  writeHeat();

  return(0);
}

void readHeat() {
    if((arq=fopen("../../input/heat.txt","rt"))==NULL){
        printf("---> File heat.txt not found\n\nPress any button to continue\n");
        exit_tool();
    }
  fscanf(arq,"%s %s %d %s %s %s",str,str,&num_heats,str,str,str);
  for(int i = 0; i<8; i++){
    fscanf(arq, "%lf %lf %lf",&xheat[i], &yheat[i], &Heat[i]);
  }
  fclose(arq);
}

void writeHeat() {
    arq = fopen("heatTemp.txt", "w+");
    if (arq == NULL) {
        printf("---> Failed to open heatTemp.txt for writing.\n");
        exit_tool();
    }
    
    fprintf(arq, "%d\n", num_heats);
    for (int i = 0; i < 8; i++) {
        fprintf(arq, "%.0lf\n", xheat[i]);
    }
    for (int i = 0; i < 8; i++) {
        fprintf(arq, "%.0lf\n", yheat[i]);
    }
    for (int i = 0; i < 8; i++) {
        fprintf(arq, "%.1lf\n", Heat[i]);
    }
    
    fclose(arq);
}


void exit_tool(){
  printf("Simulation interrupted.\n");
  exit(1);  
}  