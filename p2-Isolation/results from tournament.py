This script evaluates the performance of the custom heuristic function by
comparing the strength of an agent using iterative deepening (ID) search with
alpha-beta pruning against the strength rating of agents using other heuristic
functions.  The `ID_Improved` agent provides a baseline by measuring the
performance of a basic agent using Iterative Deepening and the "improved"
heuristic (from lecture) on your hardware.  The `Student` agent then measures
the performance of Iterative Deepening and the custom heuristic against the
same opponents.


*************************
 Evaluating: ID_Improved 
*************************

Playing Matches:
----------
  Match 1: ID_Improved vs   Random    	Result: 19 to 1
  Match 2: ID_Improved vs   MM_Null   	Result: 17 to 3
  Match 3: ID_Improved vs   MM_Open   	Result: 13 to 7
  Match 4: ID_Improved vs MM_Improved 	Result: 14 to 6
  Match 5: ID_Improved vs   AB_Null   	Result: 15 to 5
  Match 6: ID_Improved vs   AB_Open   	Result: 9 to 11
  Match 7: ID_Improved vs AB_Improved 	Result: 11 to 9


Results:
----------
ID_Improved         70.00%

*************************
   Evaluating: Student   
*************************

Playing Matches:
----------
  Match 1:   Student   vs   Random    	Result: 18 to 2
  Match 2:   Student   vs   MM_Null   	Result: 19 to 1
  Match 3:   Student   vs   MM_Open   	Result: 16 to 4
  Match 4:   Student   vs MM_Improved 	Result: 14 to 6
  Match 5:   Student   vs   AB_Null   	Result: 18 to 2
  Match 6:   Student   vs   AB_Open   	Result: 13 to 7
  Match 7:   Student   vs AB_Improved 	Result: 8 to 12


Results:
----------
Student             75.71%

*************************
 Evaluating: ID_Improved 
*************************

Playing Matches:
----------
  Match 1: ID_Improved vs   Random    	Result: 19 to 1
  Match 2: ID_Improved vs   MM_Null   	Result: 20 to 0
  Match 3: ID_Improved vs   MM_Open   	Result: 11 to 9
  Match 4: ID_Improved vs MM_Improved 	Result: 12 to 8
  Match 5: ID_Improved vs   AB_Null   	Result: 17 to 3
  Match 6: ID_Improved vs   AB_Open   	Result: 13 to 7
  Match 7: ID_Improved vs AB_Improved 	Result: 10 to 10


Results:
----------
ID_Improved         72.86%

*************************
   Evaluating: Student   
*************************

Playing Matches:
----------
  Match 1:   Student   vs   Random    	Result: 20 to 0
  Match 2:   Student   vs   MM_Null   	Result: 20 to 0
  Match 3:   Student   vs   MM_Open   	Result: 13 to 7
  Match 4:   Student   vs MM_Improved 	Result: 12 to 8
  Match 5:   Student   vs   AB_Null   	Result: 17 to 3
  Match 6:   Student   vs   AB_Open   	Result: 13 to 7
  Match 7:   Student   vs AB_Improved 	Result: 13 to 7


Results:
----------
Student             77.14%

*************************
 Evaluating: ID_Improved 
*************************

Playing Matches:
----------
  Match 1: ID_Improved vs   Random    	Result: 19 to 1
  Match 2: ID_Improved vs   MM_Null   	Result: 19 to 1
  Match 3: ID_Improved vs   MM_Open   	Result: 14 to 6
  Match 4: ID_Improved vs MM_Improved 	Result: 14 to 6
  Match 5: ID_Improved vs   AB_Null   	Result: 18 to 2
  Match 6: ID_Improved vs   AB_Open   	Result: 8 to 12
  Match 7: ID_Improved vs AB_Improved 	Result: 9 to 11


Results:
----------
ID_Improved         72.14%

*************************
   Evaluating: Student   
*************************

Playing Matches:
----------
  Match 1:   Student   vs   Random    	Result: 18 to 2
  Match 2:   Student   vs   MM_Null   	Result: 20 to 0
  Match 3:   Student   vs   MM_Open   	Result: 17 to 3
  Match 4:   Student   vs MM_Improved 	Result: 17 to 3
  Match 5:   Student   vs   AB_Null   	Result: 14 to 6
  Match 6:   Student   vs   AB_Open   	Result: 13 to 7
  Match 7:   Student   vs AB_Improved 	Result: 10 to 10


Results:
----------
Student             77.86%
