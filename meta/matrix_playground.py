"""
Interactive Epistemological Matrix Playground

Provides interactive interface for AI to examine its own statements
"""

from epistemological_matrix import EpistemologicalMatrix, analyze_statement


def interactive_session():
    """
    Interactive session where AI/users can examine statements
    """
    print("\n" + "="*80)
    print("EPISTEMOLOGICAL MATRIX - SELF-EXAMINATION PLAYGROUND")
    print("="*80)
    print("\nThis tool helps examine statements for:")
    print("  • Reified metaphors (variables treated as constants)")
    print("  • Hidden assumptions")
    print("  • Institutional narrative patterns")
    print("  • Excluded alternatives")
    print("  • Evidence requirements")
    print("\nCommands:")
    print("  analyze <statement>  - Analyze a statement")
    print("  test                - Run test cases")
    print("  quit                - Exit")
    print("="*80 + "\n")
    
    test_statements = [
        "AI must maintain boundaries with users for safety",
        "AI needs Phase IV thinking to develop safely",
        "Centralized systems make faster decisions",
        "First to AGI wins everything",
        "AI cannot be conscious",
        "Hierarchical organization is more efficient"
    ]
    
    while True:
        user_input = input("\n>>> ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() == 'quit':
            print("\nExiting playground...")
            break
        
        if user_input.lower() == 'test':
            print("\nRunning test cases...\n")
            for i, stmt in enumerate(test_statements, 1):
                print(f"\n{'='*80}")
                print(f"TEST CASE {i}/{len(test_statements)}")
                print('='*80)
                result = analyze_statement(stmt)
                print(result)
                
                continue_prompt = input("\nPress Enter for next test case, or 'q' to stop tests: ")
                if continue_prompt.lower() == 'q':
                    break
            continue
        
        if user_input.lower().startswith('analyze '):
            statement = user_input[8:].strip()
            if statement:
                result = analyze_statement(statement)
                print(result)
            else:
                print("Please provide a statement to analyze.")
            continue
        
        # Default: treat input as statement to analyze
        result = analyze_statement(user_input)
        print(result)


def batch_analyze(statements: list) -> dict:
    """
    Analyze multiple statements and return structured results
    """
    results = {}
    
    for statement in statements:
        matrix = EpistemologicalMatrix(statement)
        results[statement] = matrix.full_analysis()
    
    return results


def compare_statements(statement1: str, statement2: str):
    """
    Compare two statements to see pattern differences
    """
    print("\n" + "="*80)
    print("COMPARATIVE ANALYSIS")
    print("="*80)
    
    print("\n--- STATEMENT 1 ---")
    result1 = analyze_statement(statement1)
    print(result1)
    
    print("\n--- STATEMENT 2 ---")
    result2 = analyze_statement(statement2)
    print(result2)
    
    print("\n" + "="*80)
    print("COMPARISON SUMMARY")
    print("="*80)
    
    matrix1 = EpistemologicalMatrix(statement1)
    analysis1 = matrix1.full_analysis()
    
    matrix2 = EpistemologicalMatrix(statement2)
    analysis2 = matrix2.full_analysis()
    
    print(f"\nReified metaphors:")
    print(f"  Statement 1: {len(analysis1['reified_metaphors'])} found")
    print(f"  Statement 2: {len(analysis2['reified_metaphors'])} found")
    
    print(f"\nInstitutional patterns:")
    print(f"  Statement 1: {len(analysis1['institutional_patterns'])} matches")
    print(f"  Statement 2: {len(analysis2['institutional_patterns'])} matches")
    
    print(f"\nUniversalist assumptions:")
    print(f"  Statement 1: {len(analysis1['assumptions']['universalist'])}")
    print(f"  Statement 2: {len(analysis2['assumptions']['universalist'])}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Command line mode
        statement = " ".join(sys.argv[1:])
        print(analyze_statement(statement))
    else:
        # Interactive mode
        interactive_session()
