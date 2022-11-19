/*
 @file Managemnt_projet.c

 * @author MedAmine JABOTE & Teddy RONCIN

 * @brief gantt_PERT fonctions pour logiciel gestion des projets

 * @version 0.1

 * @date   25/09/2022
 *
 * @copyright Copyright (c) 2022
 *
*/


#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>


typedef struct Tasks {
    char* name;
    struct Tasks **successors;
    struct Tasks **ancestors;
    int id;
    int successorCount;
    int ancestorCount;
    int index;
    int duration;
    int earlier;
    int later;
} Tasks;
/*
* @brief Application de gantt_pert permet d'effectuer les calculs nécessaires pour gérer des diagrammes de Gantt et PERT
 *
 * @param taskCount: Nombre des tâches.
 * @param Tasks: type de variables tâches .
 * @param seccesors: liste des seccesseurs.
 * @param ancestors: liste des prédecesseurs
 * @param 
 * @param ordre
 * @return Return in python the diagramme de gantt et PERT.
*/
void fill_indice(Tasks *firstTask,Tasks *lastTask, int *firstTaskIndex, int* lastTaskIndex)
{
    firstTask->index = *firstTaskIndex;
    (*firstTaskIndex)++;
    while (firstTask->successorCount == 1 && lastTask->id != firstTask->id) 
    {
        firstTask = firstTask->successors[0];
        firstTask->index = *firstTaskIndex;
        (*firstTaskIndex)++;
    }

    if (lastTask->id == firstTask->id) {
        return;
    }
    lastTask->index = *lastTaskIndex;
    (*lastTaskIndex)--;
    while(lastTask->ancestorCount == 1)
    {
        lastTask = lastTask->ancestors[0];
        lastTask->index = *lastTaskIndex;
        (*lastTaskIndex)--;
    }

    for (int i = 0; i < firstTask->successorCount; i++) {
        fill_indice(firstTask->successors[i], lastTask->ancestors[i], firstTaskIndex, lastTaskIndex);
    }

}

void add_successor(Tasks* taskAnc, Tasks* taskSucc) {
    taskAnc->successors[(taskAnc->successorCount)++] = taskSucc;
    taskSucc->ancestors[(taskSucc->ancestorCount)++] = taskAnc;
}

void calculate_earlier_later(Tasks *task, int *earlier, int *later) {
    if (task->earlier != -1) {
        *earlier = task->earlier;
        *later = task->later;
        return;
    }
    if (task->ancestorCount == 0) {
        task->earlier = 0;
        task->later = 0;
        *earlier = 0;
        *later = 0;
        return;
    }
    int earlierAnc = 0;
    int laterAnc = 0;
    for (int i = 0; i < task->ancestorCount; i++) {
        calculate_earlier_later(task->ancestors[i], &earlierAnc, &laterAnc);
        if (earlierAnc > *earlier) {
            *earlier = earlierAnc;
        }
        if (laterAnc > *later) {
            *later = laterAnc;
        }
    }
    task->earlier = *earlier + task->duration;
    task->later = *later + task->duration;
    *earlier = task->earlier;
    *later = task->later;
}

void Identify_critical_tasks(Tasks* task, int* criticalTasks, int* criticalTaskCount) {
    if (task->earlier == task->later) {
        criticalTasks[(*criticalTaskCount)++] = task->id;
    for (int i = 0; i < task->successorCount; i++) {
        Identify_critical_tasks(task->successors[i], criticalTasks, criticalTaskCount);
    }
    }

}




int main()
{   
 return 0;
}
