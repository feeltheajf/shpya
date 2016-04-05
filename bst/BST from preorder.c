/*input
7
4 2 1 3 6 5 7
*/
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
 
int preorderIndex = 0;

struct node
{
   int data;
   struct node *left;
   struct node *right;
};
 
struct node* createNode(int data)
{
   struct node *temp = (struct node*) malloc(sizeof(struct node));
 
   temp->data = data;
   temp->left = temp->right = NULL;
 
   return temp;
}

void destructTree(struct node *root) 
{
   if (root == NULL)
      return;
   destructTree(root->left);
   destructTree(root->right);
   free(root);
}
 
struct node* buildTree(int preorder[], int* preorderIndex, int min, int max, int size)
{
   int key = preorder[*preorderIndex];
   if(*preorderIndex >= size)
        return NULL;
  
   struct node *root = NULL;
  
   if(key >= min && key < max)
   {
         root = createNode (key);
         *preorderIndex = *preorderIndex + 1;
         if (*preorderIndex < size)
         {
            root->left = buildTree(preorder, preorderIndex, min, key, size);
  
            root->right = buildTree(preorder, preorderIndex, key, max, size);
         }
   }
  
   return root;
}

void postorder(struct node *root) 
{
   if (root == NULL)
      return;
   postorder(root->left);
   postorder(root->right);
   printf("%d ", root->data);  
}
 
void inorder(struct node* root)
{
   if (root == NULL)
      return;
   inorder(root->left);
   printf("%d ", root->data);
   inorder(root->right);
}
 
int main ()
{
   int size;
   scanf("%i", &size);

   int *preorder;
   preorder = (int*) malloc(size * sizeof(int));

   for (int i = 0; i < size; ++i)
   {
      scanf("%i", &preorder[i]);
   }
   
   struct node *root = buildTree(preorder, &preorderIndex, INT_MIN, INT_MAX, size);

   postorder(root);
   printf("\n");
   inorder(root);
 
   destructTree(root);
   free(preorder);
   return 0;
}

