const mysql = require('mysql');

module.exports = {
  createPool: function (config) {

    const pool = mysql.createPool(config);
    const lib = {
      //执行查询
      async query(sql, par, conn = null) {
        if (conn == null) {
          conn = await new Promise((resolve, reject) => {
            pool.getConnection((erro, connection) => {
              if (erro) {
                reject(erro);
                return;
              }
              resolve(connection);
            });
          });
        }

        return new Promise((resolve, reject) => {
          const info = buildSQL(sql, par);
          conn.query(info.sql, info.params, (erro, result) => {
            //释放连接
            pool.releaseConnection(conn);
            // conn.release();
            if (erro) {
              reject(erro);
              return;
            }
            resolve(result);
          });
        });
      },
      //创建事务
      async createTransaction() {

        //获取连接
        const conn = await new Promise((resolve, reject) => {
          pool.getConnection((erro, connection) => {
            if (erro) {
              reject(erro);
              return;
            }
            resolve(connection);
          });
        });
        const t = {
          begin() {
            return new Promise((resolve, reject) => {
              conn.beginTransaction((beginErro) => {
                if (beginErro) {
                  //释放连接
                  pool.releaseConnection(conn);
                  // conn.release();
                  reject(beginErro);
                  return;
                }
                resolve(t);
              });
            });
          },
          query(sql, par) {
            const info = buildSQL(sql, par);
            return new Promise((resolve, reject) => {
              conn.query(info.sql, info.params, (erro, result) => {
                if (erro) {
                  //释放连接
                  pool.releaseConnection(conn);
                  // conn.release();
                  //回滚
                  conn.rollback((rollErro) => {
                    reject(rollErro);
                  });
                  reject(erro);
                  return;
                }
                resolve(result);
              });
            });
          },
          end() {
            return new Promise((resolve, reject) => {
              conn.commit((erro, info) => {
                if (erro) {
                  //释放连接
                  pool.releaseConnection(conn);
                  // conn.release();
                  //回滚
                  conn.rollback((rollErro) => {
                    reject(rollErro);
                    return;
                  });
                  reject(erro);
                }
                resolve(info);
              });
            });
          }
        };
        return t;
      },
    };

    return lib;
  },
  escape: function(s) {
    return mysql.escape(s) 
  }
};

/**
 * 构建SQL执行参数
 * @param {*} sql
 * @param {*} par
 * @returns {sql,params}
 */
function buildSQL(sql, par) {
  //参数处理
  const arr = [];
  const parNames = sql.match(/\$\([0-9a-zA-Z\_]{1,9999}?\)/g);
  if (parNames != null) {
    for (let pName of parNames) {
      //替换参数名
      sql = sql.replace(pName, '?');
      //转换参数名
      pName = pName.replace(/\$\(([[0-9a-zA-Z\_]{1,9999}?)\)/g, '$1')
      arr.push(par[pName]);
    }
  }
  return { sql: sql, params: arr };
}