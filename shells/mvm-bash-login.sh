
export MVM_SESSION_ID=$(mvm-session)
export MVM_GLOBAL_DIR=${HOME}/.mvm/sessions/global
export MVM_SESSION_DIR=${HOME}/.mvm/sessions/local/${MVM_SESSION_ID}

test ! -d ${MVM_GLOBAL_DIR} && mkdir -p ${MVM_GLOBAL_DIR}
test ! -d ${MVM_SESSION_DIR} && mkdir -p ${MVM_SESSION_DIR}

export PATH=${MVM_GLOBAL_DIR}/bin:${MVM_GLOBAL_DIR}/sbin:${MVM_SESSION_DIR}/bin:${MVM_SESSION_DIR}/sbin:${PATH}

