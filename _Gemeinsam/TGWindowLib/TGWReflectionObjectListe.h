#ifndef _TGWReflectionObjectListe_h_
#define _TGWReflectionObjectListe_h_

// Elemente mit diesem Datentyp werden gespeichert:
#define ELEMENT_NAME TGWReflectionObject

// Diese Liste �bernimmt den Besitz ihrer Elemente (Objektzeiger wird kopiert).
// Das bedeutet: Alle Elemente werden mit dem
// Destruktor dieser Liste aus dem Speicher
// gel�scht. (delete)

// Desweiteren d�rfen keine tempor�ren Elemente
// �bergeben werden. (Elemente M�SSEN mit "new" erzeugt
// werden)

class ELEMENT_NAME;

class TGWReflectionObjectListe
{
private:
  void* dieVectorListe;

public:
  TGWReflectionObjectListe();
  TGWReflectionObjectListe(TGWReflectionObjectListe &v)
  {
    throw "Keinen Kopierkonstruktor verwenden";
  };
  
  ~TGWReflectionObjectListe();

  void operator=(TGWReflectionObjectListe v)
  {
    throw "Keinen Gleichoperator verwenden";
  };

  void push_back(ELEMENT_NAME* e);
  int size();
  void clear();
  void erase(int i);
  ELEMENT_NAME* at(int i);
  void set(int i, ELEMENT_NAME* e);    // ueberschreiben, Liste vergroessern, falls noetig
  void insert(int i, ELEMENT_NAME* e); // wegruecken, Liste vergroessern, falls noetig
};

#undef ELEMENT_NAME
#endif
