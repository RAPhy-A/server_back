from CycleLineaire import CycleLineaire
from CycleCombinaison import CycleCombinaison

if __name__ == "__main__":
    # Crée deux instances de CycleLineaire
    c1 = CycleLineaire(0.0, 10.0, 0.0, 100.0)
    c2 = CycleLineaire(10.0, 20.0, 100.0, 400.0)
    
    # Crée une instance de CycleCombinaison à partir de c1 et c2
    cycle_comb = CycleCombinaison(c1, c2)
    
    # Test de la méthode get_value sur quelques points
    print("Test de get_value:")
    print("x = 5.0 ->", cycle_comb.get_value(5.0))    # Devrait utiliser c1
    print("x = 10.0 ->", cycle_comb.get_value(10.0))  # Se situe à la frontière, utilise c2
    print("x = 15.0 ->", cycle_comb.get_value(15.0))  # Devrait utiliser c2
    
    # Test de la méthode get_values sur une liste de valeurs
    xi = [0.0, 5.0, 9.9, 10.0, 15.0, 20.0]
    yi = cycle_comb.get_values(xi)
    print("\nTest de get_values:")
    for x, y in zip(xi, yi):
        print(f"x = {x} -> y = {y}")
