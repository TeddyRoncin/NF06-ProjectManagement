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
    int marge;
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

void task_earlier(Tasks* task) {
    task->earlier = 0
        for (int i = 0; i < task->ancestorCount; i++) {
            if (task->earlier < task->ancestors[i]->earlier + task->ancestors[i]->duration) {
            task->earlier = task->ancestors[i]->earlier + task->ancestors[i]->duration;
            }
        }
        for (int i = 0; i < task->successorCount; i++) {
            task_earlier(task->successors[i]);
        }
        
    }


void task_later(Tasks* task) {
    if (task->successorCount == 0) {
        task->later = task->earlier;
    }
    else {
        task->later = task->successors[0]->later - task->duration;
        for (int i = 1; i < task->successorCount; i++) {
            if (task->later > task->successors[i]->later - task->duration) {
                task->later = task->successors[i]->later - task->duration;
            }
        }
    }
    for (int i = 0; i < task->ancestorCount; i++) {
        task_later(task->ancestors[i]);
    }
}


bool Identify_critical_path(Tasks* task, int* criticalTasks, int* criticalTaskCount) {
    if (task->earlier == task->later) {
        criticalTasks[(*criticalTaskCount)++] = task->id;
        bool found_critical = false;
        for (int i = 0; i < task->successorCount && !found_critical; i++ ) {
            found_critical = Identify_critical_path(task->successors[i], criticalTasks, criticalTaskCount);
        }
        return true;
    }
    return false;

}


void calculate_marge(Tasks* task, int* marge) {
    if (task->earlier != task->later) {
        task->marge = task->later - task->earlier;
    }
    else if (task->earlier == task->later) {
         task->marge= 0;
    }
    for (int i = 0; i < task->successorCount; i++) {
        calculate_marge(task->successors[i], marge);
    }
}

void Gantt_chart(Tasks* task, int* Gantt, int* ordreCount) {
    //vérifier si task fait partie de la liste des tâches critiques
    if (task->earlier == task->later) {
        Gantt[task->index] = task->id;
    }
    for (int i = 0; i < task->successorCount; i++) {
        Gantt_chart(task->successors[i], Gantt, ordreCount);
    }
}


int main()
{
    Tasks* taskSucc1[1];
    Tasks* taskSucc2[2];
    Tasks* taskSucc3[2];
    Tasks* taskSucc4[1];
    Tasks* taskSucc5[1];
    Tasks* taskSucc6[1];
    Tasks* taskSucc7[1];
    Tasks* taskSucc8[0];
    Tasks* taskSucc9[1];
    Tasks* taskSucc10[1];
    Tasks* taskAnc1[0];
    Tasks* taskAnc2[1];
    Tasks* taskAnc3[1];
    Tasks* taskAnc4[1];
    Tasks* taskAnc5[1];
    Tasks* taskAnc6[2];
    Tasks* taskAnc7[2];
    Tasks* taskAnc8[1];
    Tasks* taskAnc9[1];
    Tasks* taskAnc10[1];
    Tasks task1 = {.id=1, .successors=taskSucc1, .ancestors=taskAnc1, .duration=10};
    Tasks task2 = {.id=2, .successors=taskSucc2, .ancestors=taskAnc2, .duration=10};
    Tasks task3 = {.id=3, .successors=taskSucc3, .ancestors=taskAnc3, .duration=10};
    Tasks task4 = {.id=4, .successors=taskSucc4, .ancestors=taskAnc4, .duration=10};
    Tasks task5 = {.id=5, .successors=taskSucc5, .ancestors=taskAnc5, .duration=10};
    Tasks task6 = {.id=6, .successors=taskSucc6, .ancestors=taskAnc6, .duration=10};
    Tasks task7 = {.id=7, .successors=taskSucc7, .ancestors=taskAnc7, .duration=10};
    Tasks task8 = {.id=8, .successors=taskSucc8, .ancestors=taskAnc8, .duration=10};
    Tasks task9 = {.id=9, .successors=taskSucc9, .ancestors=taskAnc9, .duration=10};
    Tasks task10 = {.id=10, .successors=taskSucc10, .ancestors=taskAnc10, .duration=10};
    
    add_successor(&task1, &task2);
    add_successor(&task2, &task3);
    add_successor(&task3, &task4);
    add_successor(&task4, &task6);
    add_successor(&task3, &task5);
    add_successor(&task5, &task6);
    add_successor(&task6, &task7);
    add_successor(&task7, &task8);
    add_successor(&task2, &task10);
    add_successor(&task10, &task9);
    add_successor(&task9, &task7);
    
    int firstTaskIndex = 0, lastTaskIndex = 9;
    fill_indice(&task1, &task8, &firstTaskIndex, &lastTaskIndex);
    printf("%d %d %d %d %d %d %d %d %d %d\n", task1.index, task2.index, task3.index, task4.index, task5.index, task6.index, task7.index, task8.index, task9.index, task10.index);
    int earlier = 100, later = 100;
    calculate_earlier_later(&task8, &earlier, &later);
    printf("%d %d %d %d %d %d %d %d %d %d\n", task1.earlier, task2.earlier, task3.earlier, task4.earlier, task5.earlier, task6.earlier, task7.earlier, task8.earlier, task9.earlier, task10.earlier);
    printf("%d %d %d %d %d %d %d %d %d %d\n", task1.later, task2.later, task3.later, task4.later, task5.later, task6.later, task7.later, task8.later, task9.later, task10.later);
    return 0;
}
