/*
 @file Managemnt_projet.c
 * @author MedAmine JABOTE & Teddy RONCIN
 * @brief gantt_PERT fonctions pour logiciel gestion des projets
 * @version 0.1
 * @date  25/09/2022
 * @copyright Copyright (c) 2022
*/


#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

// struct for tasks
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
    bool isCritical;
} Tasks;
/*
* @brief Gantt pert application allows you to perform the calculations needed to create Gantt and PERT charts
 * @param |X|Count: Numbre of X (Example: successorCount: Number of successors ).
 * @param Tasks: type of task variables.
 * @param seccesors: list of successors.
 * @param ancestors: list of predecessors
 * @param id: id of task.
 * @param index: index of task.
 * @param duration: duration of task.
 * @param earlier: earlier of task.
 * @param later: later of task.
 * @param isCritical: isCritical of task.
 * @return Return in python the diagramme de gantt and PERT.
*/

// function to add an index to a task
void fill_indice(Tasks *firstTask,Tasks *lastTask, int *firstTaskIndex, int* lastTaskIndex)
{
    // we add the index to the first task
    firstTask->index = *firstTaskIndex;
    (*firstTaskIndex)++;
    // we check if the first task is the same as the last task
    while (firstTask->successorCount == 1 && lastTask->id != firstTask->id) 
    {
        firstTask = firstTask->successors[0];
        firstTask->index = *firstTaskIndex;
        (*firstTaskIndex)++;
    }
    // we check if the last task is the same as the first task
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
    // we call the function recursively for the successors
    for (int i = 0; i < firstTask->successorCount; i++) {
        fill_indice(firstTask->successors[i], lastTask->ancestors[i], firstTaskIndex, lastTaskIndex);
    }

}

// function to add a successor to a task
void add_successor(Tasks* taskAnc, Tasks* taskSucc) {
    // we add the successor to the list of successors of the task
    taskAnc->successors[(taskAnc->successorCount)++] = taskSucc;
    taskSucc->ancestors[(taskSucc->ancestorCount)++] = taskAnc;
}

// function to calculate early-Start to each task
void task_earlier(Tasks* task) {
    task->earlier = 0;
    for (int i = 0; i < task->ancestorCount; i++) {
        //  we calculate the earliest start of the task by adding the duration of the predecessors to the earliest start of the predecessors
        if (task->earlier < task->ancestors[i]->earlier + task->ancestors[i]->duration) {
        task->earlier = task->ancestors[i]->earlier + task->ancestors[i]->duration;
        }
    }
    // we call the function recursively for the successors
    for (int i = 0; i < task->successorCount; i++) {
        task_earlier(task->successors[i]);
    }
        
}

// function to calculate late-Start to each task
void task_later(Tasks* task) {
    // we check if the task is the last task
    if (task->successorCount == 0) {
        task->later = task->earlier;
    }
    // we calculate the latest start of the task by subtracting the duration of the task to the earliest start of the successors 
    else {
        task->later = task->successors[0]->later - task->duration;
        // we check if the latest start of the task is greater than the latest start of the successors
        for (int i = 1; i < task->successorCount; i++) {
            if (task->later > task->successors[i]->later - task->duration) {
                task->later = task->successors[i]->later - task->duration;
            }
        }
    }
    // we call the function recursively for the predecessors
    for (int i = 0; i < task->ancestorCount; i++) {
        task_later(task->ancestors[i]);
    }
}

// function to identify critical tasks
void identify_critical(Tasks* task) {
    // we check if the earliest start of the task is equal to the latest start of the task
    if (task->earlier == task->later) {
        task->isCritical = true;
    }
    // we call the function recursively for the successors
    for (int i = 0; i < task->successorCount; i++) {
        identify_critical(task->successors[i]);
    }
}

// Test
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
    Tasks task1 = {.id=1, .successors=taskSucc1, .ancestors=taskAnc1};
    Tasks task2 = {.id=2, .successors=taskSucc2, .ancestors=taskAnc2};
    Tasks task3 = {.id=3, .successors=taskSucc3, .ancestors=taskAnc3};
    Tasks task4 = {.id=4, .successors=taskSucc4, .ancestors=taskAnc4};
    Tasks task5 = {.id=5, .successors=taskSucc5, .ancestors=taskAnc5};
    Tasks task6 = {.id=6, .successors=taskSucc6, .ancestors=taskAnc6};
    Tasks task7 = {.id=7, .successors=taskSucc7, .ancestors=taskAnc7};
    Tasks task8 = {.id=8, .successors=taskSucc8, .ancestors=taskAnc8};
    Tasks task9 = {.id=9, .successors=taskSucc9, .ancestors=taskAnc9};
    Tasks task10 = {.id=10, .successors=taskSucc10, .ancestors=taskAnc10};
    
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
    printf("%d %d %d %d %d %d %d %d %d %d", task1.index, task2.index, task3.index, task4.index, task5.index, task6.index, task7.index, task8.index, task9.index, task10.index);
    
    return 0;
}
