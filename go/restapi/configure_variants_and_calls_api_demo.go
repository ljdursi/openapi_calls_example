// Code generated by go-swagger; DO NOT EDIT.

package restapi

import (
    "crypto/tls"
    "net/http"
    "time"

    errors "github.com/go-openapi/errors"
    runtime "github.com/go-openapi/runtime"
    strfmt "github.com/go-openapi/strfmt"
    middleware "github.com/go-openapi/runtime/middleware"
    graceful "github.com/tylerb/graceful"

    "github.com/jinzhu/gorm"
    _ "github.com/jinzhu/gorm/dialects/sqlite"

    "github.com/ljdursi/openapi_calls_example/go/restapi/operations"
    "github.com/ljdursi/openapi_calls_example/go/models"
)

type ORMIndividual struct {
    ID uint `gorm:"primary_key,type:integer"`
    Description *string `gorm:"type:varchar(100)"`
    Created time.Time
}

func (o *ORMIndividual) from_Swagger (m models.Individual) {
    o.Description = m.Description
    o.Created = time.Time(m.Created)
    o.ID = uint(m.ID)
}

func (o ORMIndividual) to_Swagger() *models.Individual {
    m := new(models.Individual)
    m.Description = o.Description
    m.Created = strfmt.DateTime(o.Created)
    m.ID = int64(o.ID)
    return m
}

type ORMVariant struct {
    ID uint `gorm:"type:integer,primary_key"`
    Chromosome string `gorm:"type:varchar(10)"`
    Name *string `gorm:"type:varchar(100)"`
    Alt string `gorm:"type:varchar(100)"`
    Ref string `gorm:"type:varchar(100)"`
    Start uint `gorm:"type:integer"`
}

func (o *ORMVariant) from_Swagger (m models.Variant) {
    o.ID = uint(m.ID)
    o.Chromosome = *m.Chromosome
    o.Name = m.Name
    o.Ref = *m.Ref
    o.Alt = *m.Alt
    o.Start = uint(*m.Start)
}

func (o ORMVariant) to_Swagger() *models.Variant {
    m := new(models.Variant)
    m.Chromosome = &o.Chromosome
    m.ID = int64(o.ID)
    m.Name = o.Name
    m.Ref = &o.Ref
    m.Alt = &o.Alt
    s := int64(o.Start)
    m.Start = &s
    return m
}

type ORMCall struct {
    ID uint `gorm:"primary_key,type:integer"`
    Format *string `gorm:"type:varchar(100)"`
    Genotype string `gorm:"type:varchar(20)"`
    IndividualID uint
    VariantID uint
    Created *time.Time
}

func (o *ORMCall) from_Swagger (m models.Call) {
    t := time.Time(m.Created)
    o.Created = &t
    o.ID = uint(m.ID)
    o.Format = m.Format
    o.Genotype = *m.Genotype
    o.IndividualID = uint(*m.IndividualID)
    o.VariantID = uint(*m.VariantID)
}

func (o ORMCall) to_Swagger() *models.Call {
    m := new(models.Call)
    m.ID = int64(o.ID)
    m.Created = strfmt.DateTime(*o.Created)
    m.Format = o.Format
    m.Genotype = &o.Genotype
    iid := int64(o.IndividualID)
    vid := int64(o.VariantID)
    m.IndividualID = &iid
    m.VariantID = &vid
    return m
}


//go:generate swagger generate server --target .. --name  --spec ../swagger.yaml

func configureFlags(api *operations.VariantsAndCallsAPIDemoAPI) {
    // api.CommandLineOptionsGroups = []swag.CommandLineOptionsGroup{ ... }
}

var db *gorm.DB

func configureAPI(api *operations.VariantsAndCallsAPIDemoAPI) http.Handler {
    db, err := gorm.Open("sqlite3", "api.db")
    if err != nil {
      panic("failed to connect database")
    }
    // Create the schema
    db.CreateTable(&ORMIndividual{})
    db.CreateTable(&ORMVariant{})
    db.CreateTable(&ORMCall{})

    // configure the api here
    api.ServeError = errors.ServeError

    // Set your custom logger if needed. Default one is log.Printf
    // Expected interface func(string, ...interface{})
    //
    // Example:
    // api.Logger = log.Printf

    api.JSONConsumer = runtime.JSONConsumer()

    api.JSONProducer = runtime.JSONProducer()

    api.MainGetCallsHandler = operations.MainGetCallsHandlerFunc(func(params operations.MainGetCallsParams) middleware.Responder {
        var ocs []ORMCall
        db.Find(&ocs)

        mcs := make([]*models.Call, len(ocs))
        for idx, oc := range(ocs) {
            mcs[idx] = oc.to_Swagger()
        }
        return operations.NewMainGetCallsOK().WithPayload(mcs)
    })
    api.MainGetIndividualsHandler = operations.MainGetIndividualsHandlerFunc(func(params operations.MainGetIndividualsParams) middleware.Responder {
        var ois []ORMIndividual
        db.Find(&ois)

        mis := make([]*models.Individual, len(ois))
        for idx, oi := range(ois) {
            mis[idx] = oi.to_Swagger()
        }
        return operations.NewMainGetIndividualsOK().WithPayload(mis)
    })
    api.MainGetIndividualsByVariantHandler = operations.MainGetIndividualsByVariantHandlerFunc(func(params operations.MainGetIndividualsByVariantParams) middleware.Responder {
        var vrnt ORMVariant;
        db.First(&vrnt, params.VariantID)

        var icalls []ORMCall
        db.Where(&ORMCall{VariantID: vrnt.ID}).Find(&icalls);
        minds := make([]*models.Individual, len(icalls))

        for idx, call := range icalls {
            var i ORMIndividual
            db.Where(&ORMIndividual{ID: call.IndividualID}).First(&i)
            minds[idx] = i.to_Swagger()
        }
        return operations.NewMainGetIndividualsByVariantOK().WithPayload(minds)
    })
    api.MainGetVariantsHandler = operations.MainGetVariantsHandlerFunc(func(params operations.MainGetVariantsParams) middleware.Responder {
        var ovs []ORMVariant
        db.Find(&ovs)

        mvs := make([]*models.Variant, len(ovs))
        for idx, ov := range(ovs) {
            mvs[idx] = ov.to_Swagger()
        }
        return operations.NewMainGetVariantsOK().WithPayload(mvs)
    })
    api.MainGetVariantsByIndividualHandler = operations.MainGetVariantsByIndividualHandlerFunc(func(params operations.MainGetVariantsByIndividualParams) middleware.Responder {
        var ind ORMIndividual;
        db.First(&ind, params.IndividualID)

        var icalls []ORMCall
        db.Where(&ORMCall{IndividualID: ind.ID}).Find(&icalls);
        mvars := make([]*models.Variant, len(icalls))

        for idx, call := range icalls {
            var v ORMVariant
            db.Where(&ORMVariant{ID: call.VariantID}).First(&v)
            mvars[idx] = v.to_Swagger()
        }
        return operations.NewMainGetVariantsByIndividualOK().WithPayload(mvars)
    })
    api.MainPutCallHandler = operations.MainPutCallHandlerFunc(func(params operations.MainPutCallParams) middleware.Responder {
        var v ORMCall
        v.from_Swagger(*params.Call)
        db.Create(&v)
        return operations.NewMainPutCallCreated()
    })
    api.MainPutIndividualHandler = operations.MainPutIndividualHandlerFunc(func(params operations.MainPutIndividualParams) middleware.Responder {
        var i ORMIndividual
        i.from_Swagger(*params.Individual)
        db.Create(&i)
        return operations.NewMainPutIndividualCreated()
    })
    api.MainPutVariantHandler = operations.MainPutVariantHandlerFunc(func(params operations.MainPutVariantParams) middleware.Responder {
        var v ORMVariant
        v.from_Swagger(*params.Variant)
        db.Create(&v)
        return operations.NewMainPutVariantCreated()
    })

    api.ServerShutdown = func() {}

    return setupGlobalMiddleware(api.Serve(setupMiddlewares))
}

// The TLS configuration before HTTPS server starts.
func configureTLS(tlsConfig *tls.Config) {
    // Make all necessary changes to the TLS configuration here.
}


// As soon as server is initialized but not run yet, this function will be called.
// If you need to modify a config, store server instance to stop it individually later, this is the place.
// This function can be called multiple times, depending on the number of serving schemes.
// scheme value will be set accordingly: "http", "https" or "unix"
func configureServer(s *graceful.Server, scheme, addr string) {
}

// The middleware configuration is for the handler executors. These do not apply to the swagger.json document.
// The middleware executes after routing but before authentication, binding and validation
func setupMiddlewares(handler http.Handler) http.Handler {
    return handler
}

// The middleware configuration happens before anything, this middleware also applies to serving the swagger.json document.
// So this is a good place to plug in a panic handling middleware, logging and metrics
func setupGlobalMiddleware(handler http.Handler) http.Handler {
    return handler
}
