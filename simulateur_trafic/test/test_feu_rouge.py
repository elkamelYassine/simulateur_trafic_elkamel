from simulateur_trafic.models.feu_rouge import FeuRouge

def test_cycle_du_feu():
    """
    Test de la succession des états du feu rouge.
    """
    
    feu = FeuRouge(cycle=10)
    
    assert feu.etat == "rouge"
    
    feu.avancer_temps(2)
    assert feu.etat == "rouge"
    
    feu.avancer_temps(3)
    assert feu.etat == "vert"
    
    feu.avancer_temps(2)
    assert feu.etat == "vert"
    
    feu.avancer_temps(2)
    assert feu.etat == "orange"
    
    feu.avancer_temps(1.5)
    assert feu.etat == "rouge"
