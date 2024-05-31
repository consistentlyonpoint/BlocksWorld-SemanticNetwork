from SemanticNetsAgent import SemanticNetsAgent
from SemanticNetsAgent_LoTR import SemanticNetsAgent
#from SemanticNetsAgent_NoPrint import SemanticNetsAgent
#from SemanticNetsAgent_new import SemanticNetsAgent

def test():
    #This will test your SemanticNetsAgent
	#with seven initial test cases.
    #test_agent = SemanticNetsAgent()
    #test_agent = SemanticNetsAgent()
    test_lotr_agent = SemanticNetsAgent()

    # print(test_agent.solve(1, 1))
    # print(1)
    # print(test_agent.solve(2, 2))
    # print(2)
    # print(test_agent.solve(3, 3))
    # print(3)
    # print(test_agent.solve(5, 3))
    # print(4)
    # print(test_agent.solve(6, 3))
    # print(5)
    # print(test_agent.solve(7, 3))
    # print(6)
    # print(test_agent.solve(5, 5))
    # print(7)
    print(test_lotr_agent.solve(1, 1, 1, 1))

if __name__ == "__main__":
    test()
