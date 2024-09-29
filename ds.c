#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//structure
typedef struct TreeNode
{
	int key;
	char* data;
	struct TreeNode* left;
	struct TreeNode* right;
} TreeNode;

//create
TreeNode* createNode(int key, const char* data)
{
	TreeNode* newNode = (TreeNode*)malloc(sizeof(TreeNode));
	
	if (newNode == NULL)
	{
		perror("Memory allocation failed");
		exit(EXIT_FAILURE);
	}

	newNode->key = key;
	newNode->data = strdup(data);

	if (newNode->data == NULL)
	{
		perror("Memory allocation failed");
		exit(EXIT_FAILURE);
	}

	newNode->left = newNode->right = NULL;
	return newNode;
}

//insert
TreeNode* insert(TreeNode* root, int key, const char* data)
{
	if (root == NULL)
	{
		return createNode(key, data);
	}

	if (key < root->key)
	{
		root->left = insert(root->left, key, data);
	}
	else if (key > root->key)
	{
		root->right = insert(root->right, key, data);
	}
	else
	{
		printf("[insert] duplicated key %d\n", key);
	}
	
	return root;
}

//search
TreeNode* search(TreeNode* root, int key)
{
	if (root == NULL)
	{
		printf("[search] non-existing key %d\n", key);
		return NULL;
	}
	if (root->key == key)
	{
		return root;
	}

	if (key < root->key)
	{
		return search(root->left, key);
	}

	return search(root->right, key);
}

//delete
TreeNode* deleteNode(TreeNode* root, int key)
{
	if (root == NULL)
	{
		printf("[delete] non-existing key %d\n", key);
		return NULL;
	}

	if (key < root->key)
	{
		root->left = deleteNode(root->left, key);
	}
	else if (key > root->key)
	{
		root->right = deleteNode(root->right, key);
	}
	else
	{
		if (root->left == NULL)
		{
			TreeNode* temp = root->right;
			free(root->data);
			free(root);
			return temp;
		}
		else if (root->right == NULL)
		{
			TreeNode* temp = root->left;
			free(root->data);
			free(root);
			return temp;
		}

		TreeNode* temp = root->right;
		while (temp->left != NULL)
		{
			temp = temp->left;
		}

		root->key = temp->key;
		root->data = strdup(temp->data);
		root->right = deleteNode(root->right, temp->key);
	}

	return root;
}

//traversal
void inorderTraversal(TreeNode* root)
{
	if (root != NULL)
	{
		inorderTraversal(root->left);
		printf("(%d, %s) ", root->key, root->data);
		inorderTraversal(root->right);
	}
}

//free
void freeTree(TreeNode* root) {
    if (root != NULL) {
        freeTree(root->left);
        freeTree(root->right);
        free(root->data);
        free(root);
    }
}

int main()
{
	TreeNode* root = NULL;

	root = insert(root, 5, "ATTG");
	root = insert(root, 3, "ATGC");
	root = insert(root, 2, "TTTAAA");
	root = insert(root, 4, "GCC");
	root = insert(root, 6, "TGGGA");
	root = insert(root, 3, "AGA");

	printf("inorder : ");
	inorderTraversal(root);
	printf("\n");

	int searchKey = 5;
	TreeNode* result = search(root, searchKey);
	
	if (result != NULL)
	{
		printf("searched (%d, %s)\n", result->key, result->data);
		printf("strlen of str data(%d)=%ld\n", searchKey, strlen(result->data));
		printf("size of node(%d)=%ld\n", searchKey, sizeof(*result));
	}
	else
	{
		printf("failed to search key %d\n", searchKey);
	}

	int deleteKey = 5;
	root = deleteNode(root, deleteKey);

	printf("inorder : ");
	inorderTraversal(root);
	printf("\n");

	deleteKey = 5;
	root = deleteNode(root, deleteKey);

	printf("inorder : ");
	inorderTraversal(root);
	printf("\n");

	searchKey = 2;
	result = search(root, searchKey);
	
	if (result != NULL)
	{
		printf("searched (%d, %s)\n", result->key, result->data);
		printf("strlen of str data(%d)=%ld\n", searchKey, strlen(result->data));
		printf("size of node(%d)=%ld\n", searchKey, sizeof(*result));
	}
	else
	{
		printf("failed to search key %d\n", searchKey);
	}

	freeTree(root);

	return 0;
}