db = db.getSiblingDB("wd2t")
db.dummy.insert({})
db.createUser(
    {
    user: "wd2t_app",
    pwd: "something very secure",
    roles: [
        {
            role: "readWrite",
            db: "wd2t"
        }
    ]}
)