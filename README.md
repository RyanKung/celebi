# Celebi

###  An Actor-model based reactive time-series data analysis system.


### Project model:


$Ev := \{Datum, Ev\}$

$(.) := property(x, y) \rightarrow y$

$\alpha Actor := \{entangle, process, mailbox, spout\} $

$Actor.spout := spout(t, datum) \rightarrow queue\{data\} $

$Actor.measure := measure (t, datum_t, Ctx_t) \rightarrow measure(t+1, datum^'_{t+1})$

$Actor.entangle := entangle(actor) \rightarrow spout \circ measure(actor.spout)$

$\alpha Arbiter := \{route, list, register\}$

### Technology Selecion

`Arbiter: Flask`

`Actor Model Implementation`: `pulsar`

`Message Queue`: `RabbatMQ`

`Time-series Data Storage`: `postgres`

`Context Data Storage`: `redis`