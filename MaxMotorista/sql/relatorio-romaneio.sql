with
  por_entregas as (
    select
      entrega.codigo_motorista,
      empregado.nome as nome_motorista,
      motorista.nome as nome_usuario_app,
      veiculo.codigo_veiculo,
      veiculo.placa,
      cliente.codigo_atividade1 as codigo_atividade,
      coalesce(ramo.ramo_atividade, 'N/A') as ramo_atividade,
      entrega.numero_carregamento,
      entrega.id_entrega,
      entrega.codigo_cliente,
      cliente.razaosocial as nome_cliente,
      cliente.cidade,
      cliente.uf,
      entrega.data_termino_descarga,
      entrega.data_inicio_descarga,
      entrega.data_inicio_checkin,
      pedido.vlatend as valor_atendido,
      pedido.vlpedido as valor_total,
      pedido.peso_total as peso_total,
      pedido.volume_total as volume_total,
      carregamento.data_inicio_romaneio,
      carregamento.data_fim_romaneio,
      nota.id_nota_fiscal_motorista,
      entrega.tempo_entrega,
      empregado.codigo_filial as codigo_filial_motorista,
      pedido.codigo_filial as codigo_filial_pedido,
      entrega.raio_entrega,
      coalesce(situacao_entrega.situacao_entrega, 'N/A') as situacao_entrega,
      entrega.tolerancia_raio_entrega,
      carregamento.data_saida_carregamento,
      carregamento.data_fechamento_carregamento
    from
      fato_entregas entrega
      inner join fato_carregamentos carregamento on carregamento.numero_carregamento = entrega.numero_carregamento
      and carregamento.codigo_motorista = entrega.codigo_motorista
      inner join dim_nota_fiscal nota on nota.numero_carregamento = carregamento.numero_carregamento
      and nota.id_entrega = entrega.id_entrega
      inner join fato_pedido_realizado pedido on pedido.numero_carregamento = carregamento.numero_carregamento
      and pedido.numpederp = nota.numero_pedido
      and pedido.codigo_cliente = entrega.codigo_cliente --não tem todos os pedidos (a fato_pedido_realizado faz alguns filtros)
      inner join dim_empregado empregado on empregado.matricula = entrega.codigo_motorista
      inner join dim_veiculo veiculo on veiculo.codigo_veiculo = carregamento.codigo_veiculo
      inner join dim_usuario_motorista motorista on motorista.id_motorista = entrega.codigo_motorista
      inner join dim_cliente cliente on cliente.codigo_cliente = entrega.codigo_cliente
      left join dim_ramo_atividade ramo on ramo.codigo_atividade = cliente.codigo_atividade1
      left join dim_situacao_entrega situacao_entrega on situacao_entrega.id = entrega.id_situacao_entrega
    where
      motorista.tipo = 'M'
      and carregamento.data_inicio_romaneio BETWEEN DATE '2025-08-28' AND DATE '2025-08-28'
    group by
      entrega.codigo_motorista,
      empregado.nome,
      motorista.nome,
      veiculo.codigo_veiculo,
      veiculo.placa,
      cliente.codigo_atividade1,
      ramo.ramo_atividade,
      entrega.numero_carregamento,
      entrega.id_entrega,
      entrega.codigo_cliente,
      cliente.razaosocial,
      cliente.cidade,
      cliente.uf,
      entrega.data_termino_descarga,
      entrega.data_inicio_descarga,
      entrega.data_inicio_checkin,
      pedido.vlatend,
      pedido.vlpedido,
      pedido.peso_total,
      pedido.volume_total,
      carregamento.data_inicio_romaneio,
      carregamento.data_fim_romaneio,
      nota.id_nota_fiscal_motorista,
      entrega.tempo_entrega,
      empregado.codigo_filial,
      pedido.codigo_filial,
      entrega.raio_entrega,
      coalesce(situacao_entrega.situacao_entrega, 'N/A'),
      entrega.tolerancia_raio_entrega,
      carregamento.data_saida_carregamento,
      carregamento.data_fechamento_carregamento
  ),
  devolucao as (
    select
      id_entrega,
      sum(vldevolucao) as valor_devolucao_winthor
    from
      fato_devolucao
    group by
      id_entrega
  )
select
  por_entregas.id_entrega,
  round(sum(por_entregas.valor_atendido), 2) as valor_entrega,
  round(sum(por_entregas.peso_total), 2) as peso_entrega,
  round(sum(por_entregas.volume_total), 2) as volume_total,
  por_entregas.data_saida_carregamento,
  por_entregas.codigo_cliente,
  por_entregas.nome_cliente,
  por_entregas.cidade as cidade_cliente,
  por_entregas.uf as estado_cliente,
  por_entregas.codigo_atividade,
  por_entregas.ramo_atividade,
  por_entregas.codigo_motorista,
  por_entregas.nome_motorista,
  por_entregas.nome_usuario_app,
  por_entregas.codigo_veiculo,
  por_entregas.placa,
  por_entregas.codigo_filial_motorista,
  por_entregas.codigo_filial_pedido,
  por_entregas.numero_carregamento,
  por_entregas.situacao_entrega,
  por_entregas.data_inicio_checkin,
  por_entregas.data_inicio_descarga,
  por_entregas.data_termino_descarga,
  por_entregas.data_inicio_romaneio,
  por_entregas.data_fim_romaneio,
  round(por_entregas.tempo_entrega, 2) as tempo_entrega_em_minutos,
  por_entregas.raio_entrega as distancia_do_checkin,
  case
    when por_entregas.raio_entrega > por_entregas.tolerancia_raio_entrega then 'S'
    ELSE 'N'
  end as entrega_fora_do_raio,
  por_entregas.tolerancia_raio_entrega,
  count(por_entregas.id_nota_fiscal_motorista) as quantidade_notas_fiscais,
  max(devolucao.valor_devolucao_winthor) as valor_devolucao_winthor,
  case
    when max(devolucao.valor_devolucao_winthor) is not null then 'DEVOLVIDA'
    when por_entregas.data_fechamento_carregamento is null then 'PENDENTE DE FECHAMENTO'
    else 'ENTREGUE'
  end as status_winthor
from
  por_entregas
  left join devolucao on devolucao.id_entrega = por_entregas.id_entrega
group by
  por_entregas.id_entrega,
  por_entregas.data_saida_carregamento,
  por_entregas.codigo_cliente,
  por_entregas.nome_cliente,
  por_entregas.cidade,
  por_entregas.uf,
  por_entregas.codigo_atividade,
  por_entregas.ramo_atividade,
  por_entregas.codigo_motorista,
  por_entregas.nome_motorista,
  por_entregas.nome_usuario_app,
  por_entregas.codigo_veiculo,
  por_entregas.placa,
  por_entregas.codigo_filial_motorista,
  por_entregas.codigo_filial_pedido,
  por_entregas.numero_carregamento,
  por_entregas.situacao_entrega,
  por_entregas.data_inicio_checkin,
  por_entregas.data_inicio_descarga,
  por_entregas.data_termino_descarga,
  por_entregas.data_inicio_romaneio,
  por_entregas.data_fim_romaneio,
  round(por_entregas.tempo_entrega, 2),
  por_entregas.raio_entrega,
  por_entregas.tolerancia_raio_entrega,
  por_entregas.data_fechamento_carregamento
ORDER BY
  ID_ENTREGA;
