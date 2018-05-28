package main

import (
    "fmt"
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/sqlite"
)

type ORMIndividual struct {
    ID uint `gorm:"primary_key,type:integer"`
    Description *string `gorm:"type:varchar(100)"`
}

func (i ORMIndividual) String() string {
    return fmt.Sprintf("{ID: %d, Description: '%s'}", i.ID, *i.Description)
}

type ORMVariant struct {
    ID uint `gorm:"type:integer,primary_key"`
    Chromosome string `gorm:"type:varchar(10)"`
    Name *string `gorm:"type:varchar(100)"`
	Alt string `gorm:"type:varchar(100)"`
	Ref string `gorm:"type:varchar(100)"`
    Start uint `gorm:"type:integer"`
}

type ORMCall struct {
    ID uint `gorm:"primary_key,type:integer"`
    Format *string `gorm:"type:varchar(100)"`
    Genotype string `gorm:"type:varchar(20)"`
	IndividualID uint
	VariantID uint
}

func main() {
  db, err := gorm.Open("sqlite3", "test.db")
  if err != nil {
    panic("failed to connect database")
  }
  defer db.Close()

  // Create the schema
  db.CreateTable(&ORMIndividual{})
  db.CreateTable(&ORMVariant{})
  db.CreateTable(&ORMCall{})

  // Create
  name := "Subject X"
  db.Create(&ORMIndividual{Description: &name, ID: 1})
  name = "Subject Y"
  db.Create(&ORMIndividual{Description: &name, ID: 7})

  name = "rs699"
  db.Create(&ORMVariant{ID: 1, Name: &name, Chromosome: "chr1", Start: 230710048, Ref: "C", Alt: "T"})
  name = "rs900"
  db.Create(&ORMVariant{ID: 2, Name: &name, Chromosome: "chr1", Start: 218441563, Ref: "A", Alt: "T"})
  name = "rs5714"
  db.Create(&ORMVariant{ID: 3, Name: &name, Chromosome: "chr1", Start: 53247055, Ref: "A", Alt: "G"})

  db.Create(&ORMCall{ID: 1, IndividualID: 1, VariantID: 1, Genotype: "0/1"})
  db.Create(&ORMCall{ID: 2, IndividualID: 1, VariantID: 2, Genotype: "0/0"})
  db.Create(&ORMCall{ID: 3, IndividualID: 7, VariantID: 2, Genotype: "1/1"})
  db.Create(&ORMCall{ID: 4, IndividualID: 7, VariantID: 3, Genotype: "0/1"})

  // Read
  print("Individual 7:")
  var ind ORMIndividual;
  db.First(&ind, 7)
  fmt.Println(ind)


  print("Variant 2:")
  var vrnt ORMVariant;
  db.First(&vrnt, 2)
  fmt.Printf("%+v\n", vrnt)

  print("Variants found in individual 7:\n")
  var icalls []ORMCall
  db.Where(&ORMCall{IndividualID: ind.ID}).Find(&icalls);
  for _, call := range icalls {
      var v ORMVariant
      db.Where(&ORMVariant{ID: call.VariantID}).First(&v)
      fmt.Printf("%+v\n", v)
  }

  print("Individuals found w/ variant 2:\n")
  db.Where(&ORMCall{VariantID: vrnt.ID}).Find(&icalls);
  for _, call := range icalls {
      var i ORMIndividual
      db.Where(&ORMIndividual{ID: call.IndividualID}).First(&i)
      fmt.Println(i)
  }
}
