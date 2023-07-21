#include "TGWReflectionObjectListe.h"
#include "TGWReflectionObject.h"

#include <vector>
using std::vector;

#define ELEMENT_NAME TGWReflectionObject
#define VECTORCLASSNAME vector<ELEMENT_NAME*>
#define DIE_VEKTORLISTE  ((VECTORCLASSNAME*)dieVectorListe)

TGWReflectionObjectListe::TGWReflectionObjectListe()
{
  dieVectorListe = new VECTORCLASSNAME();
}

TGWReflectionObjectListe::~TGWReflectionObjectListe()
{
  clear();
  delete ((VECTORCLASSNAME*) dieVectorListe);
}

void TGWReflectionObjectListe::push_back(ELEMENT_NAME* r)
{
  ((VECTORCLASSNAME*) dieVectorListe)->push_back(r);
}

int TGWReflectionObjectListe::size()
{
  return ((VECTORCLASSNAME*) dieVectorListe)->size();
}

ELEMENT_NAME* TGWReflectionObjectListe::at(int i)
{
  return ((VECTORCLASSNAME*)dieVectorListe)->at(i);
}

void TGWReflectionObjectListe::clear()
{
  for (int i=0; i<size(); i++)
  {
    delete at(i);
  }

  ((VECTORCLASSNAME*)dieVectorListe)->clear();
}

void TGWReflectionObjectListe::erase(int i)
{
  delete at(i);

  VECTORCLASSNAME::iterator it = ((VECTORCLASSNAME*)dieVectorListe)->begin()+i;
  ((VECTORCLASSNAME*)dieVectorListe)->erase(it);
}

#undef ELEMENT_NAME
