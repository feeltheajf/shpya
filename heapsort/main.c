/*input
3 3
1 13 13
234 234 23
235 12 12
*/

#include <stdlib.h>
#include <stdio.h>
 
int heapsize = 0;

void push(int st[],int i)
{
    st[heapsize] = i;
    heapsize++;
}

int pop(int st[])
{
    heapsize--;
    if(heapsize < 0)
    {
       return 0;
    }
    return st[heapsize];
}

void shiftDown(int arr[], int i, int j)
{
    int done = 0;
    int maxChild;
    int temp;

    while ((i * 2 + 1 < j) && (!done))
    {
        if (i * 2 + 1 == j - 1)
            maxChild = i * 2 + 1; 
        else if (arr[i * 2 + 1] < arr[i * 2 + 2])
            maxChild = i * 2 + 1;
        else
            maxChild = i * 2 + 2;

        if (arr[i] > arr[maxChild])
        {
            temp = arr[i];
            arr[i] = arr[maxChild];
            arr[maxChild] = temp;
            i = maxChild;
        }
        else
        {
            done = 1;
        }
    }
}

void HeapSort(int arr[])
{
    int temp;

    for (int i = heapsize / 2 - 1; i >= 0; i--)
    {
        shiftDown(arr, i, heapsize);
    }

    for (int i = heapsize - 1; i >= 1; i--)
    {
        temp = arr[0];
        arr[0] = arr[i];
        arr[i] = temp;
        shiftDown(arr, 0, i);
    }
}

int main()
{
    int rows;
    int length;
    int tmp = 0;
    scanf("%i", &rows);
    scanf("%i", &length);
    int *heap;
    heap = (int*) malloc(rows * length * sizeof(int));

    for (int i = 0; i < rows; ++i)
    {
        for (int j = 0; j < length; ++j)
        {
            scanf("%i", &tmp);
            push(heap, tmp);
        }
    }

    HeapSort(heap);
    
    for (int i = 0; i < rows; ++i)
    {
        for (int j = 0; j < length; ++j)
        {
            tmp = pop(heap);
            printf("%i ", tmp);
        }
    }
    
    free(heap);
    
    return 0;
}

















