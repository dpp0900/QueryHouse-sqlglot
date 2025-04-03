import sys
from sqlglot import transpile, ErrorLevel, exp, parse_one
from sqlglot.errors import UnsupportedError
# q = "CREATE TABLE tbl_name (var1 INT);"
# print(repr(parse_one(q)))

# q = "CREATE VIRTUAL TABLE tbl_name USING fts5(column_def_commalist);"
# print(repr(parse_one(q)))

# 사용자에게 여러 줄의 쿼리 입력 받기
print("변환할 SQL 쿼리를 입력하세요 (입력이 끝나면 Ctrl+D 또는 Ctrl+Z를 누르세요):")
queries = sys.stdin.read()  # 여러 줄의 입력 받기

queries = queries.strip()  # 입력 받은 쿼리의 앞뒤 공백 제거
queries = queries.replace('\n', ' ')  # 입력 받은 쿼리의 줄바꿈 문자 제거
queries = queries.split(';')
queries.pop()

result = [[] for _ in range(4)]
try:
    # 각 DBMS에 맞게 쿼리를 변환 (오류 발생 시 즉시 예외 발생)
    for query in queries:
        print(repr(parse_one(query)))
        sqlite_query = transpile(query, write='sqlite', unsupported_level=ErrorLevel.RAISE)
        # sqlite_query =  [query]
        mysql_query = transpile(query, write='mysql', unsupported_level=ErrorLevel.RAISE)
        # mysql_query = [query]
        postgresql_query = transpile(query, write='postgres', unsupported_level=ErrorLevel.RAISE)
        oracle_query = transpile(query, write='oracle', unsupported_level=ErrorLevel.RAISE)
        mariadb_query = transpile(query, write='mariadb', unsupported_level=ErrorLevel.RAISE)
        # oracle_query = [query]

        
        for i, q in enumerate([sqlite_query, mysql_query, postgresql_query, oracle_query, mariadb_query]):
            result[i].append(q[0])

except UnsupportedError as e:
    # 변환 중 지원되지 않는 기능이 있는 경우 예외 처리
    print(f"쿼리 변환 중 오류가 발생했습니다: {e}")
    
print("INPUT: ")
for query in queries:
    print(query + ';')

print("\nSQLite:")
for query in result[0]:
    print(query + ';')

print("\nMySQL:")
for query in result[1]:
    print(query + ';')
    
print("\nPostgreSQL:")
for query in result[2]:
    print(query + ';')
    
print("\nOracle:")
for query in result[3]:
    print(query + ';')
    
print("\nMariaDB:")
for query in result[4]:
    print(query + ';')